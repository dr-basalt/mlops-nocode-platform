import unittest
import os
import sys
from unittest.mock import patch, MagicMock
import tempfile

# Ajouter le chemin du script à tester
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import cpu_throttler


class TestCpuThrottler(unittest.TestCase):

    def setUp(self):
        # Sauvegarder les variables d'environnement originales
        self.original_env = dict(os.environ)
        
        # Réinitialiser les variables d'environnement du module
        cpu_throttler.CPU_THRESHOLD = 90.0
        cpu_throttler.LOAD_AVG_THRESHOLD = 6.0
        cpu_throttler.CHECK_INTERVAL = 0.1
        cpu_throttler.MAX_WAIT_TIME = 5.0
        cpu_throttler.THROTTLE_DISABLE = False

    def tearDown(self):
        # Restaurer les variables d'environnement originales
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_get_load_avg(self):
        # Test de la fonction get_load_avg
        load_avg = cpu_throttler.get_load_avg()
        self.assertIsInstance(load_avg, float)
        self.assertGreaterEqual(load_avg, 0)

    @patch('cpu_throttler.psutil.cpu_percent')
    @patch('cpu_throttler.get_load_avg')
    def test_wait_for_cpu_and_load_availability_below_thresholds(self, mock_get_load_avg, mock_cpu_percent):
        # Tester lorsque l'utilisation CPU et le load average sont en dessous des seuils
        mock_cpu_percent.return_value = 50.0  # CPU en dessous du seuil
        mock_get_load_avg.return_value = 3.0  # Load average en dessous du seuil
        
        # Appeler la fonction
        cpu_throttler.wait_for_cpu_and_load_availability(
            cpu_threshold=80.0,
            load_avg_threshold=5.0,
            check_interval=0.01,
            max_wait_time=1.0,
            verbose=False
        )
        
        # Vérifier que psutil.cpu_percent a été appelé
        mock_cpu_percent.assert_called_once_with(interval=0.01)

    @patch('cpu_throttler.psutil.cpu_percent')
    @patch('cpu_throttler.get_load_avg')
    @patch('time.time')
    def test_wait_for_cpu_and_load_availability_above_thresholds(self, mock_time, mock_get_load_avg, mock_cpu_percent):
        # Tester lorsque l'utilisation CPU et le load average sont au-dessus des seuils
        mock_cpu_percent.return_value = 95.0  # CPU au-dessus du seuil
        mock_get_load_avg.return_value = 7.0  # Load average au-dessus du seuil
        mock_time.side_effect = [0, 0.5, 1.0, 1.5, 2.0]  # Simuler le passage du temps
        
        # Appeler la fonction avec un temps d'attente maximum court pour le test
        cpu_throttler.wait_for_cpu_and_load_availability(
            cpu_threshold=90.0,
            load_avg_threshold=6.0,
            check_interval=0.01,
            max_wait_time=1.0,
            verbose=False
        )
        
        # Vérifier que psutil.cpu_percent a été appelé plusieurs fois
        self.assertGreater(mock_cpu_percent.call_count, 1)

    @patch('cpu_throttler.psutil.cpu_percent')
    @patch('cpu_throttler.get_load_avg')
    def test_wait_for_cpu_and_load_availability_throttle_disabled(self, mock_get_load_avg, mock_cpu_percent):
        # Tester lorsque le throttling est désactivé
        cpu_throttler.THROTTLE_DISABLE = True
        
        # Appeler la fonction
        cpu_throttler.wait_for_cpu_and_load_availability(
            cpu_threshold=80.0,
            load_avg_threshold=5.0,
            check_interval=0.01,
            max_wait_time=1.0,
            verbose=False
        )
        
        # Vérifier que psutil.cpu_percent n'a pas été appelé
        mock_cpu_percent.assert_not_called()
        mock_get_load_avg.assert_not_called()

    def test_throttle_operation_throttle_disabled(self):
        # Tester throttle_operation lorsque le throttling est désactivé
        cpu_throttler.THROTTLE_DISABLE = True
        
        # Définir une opération de test
        def test_operation(x, y):
            return x + y
        
        # Appeler throttle_operation
        result = cpu_throttler.throttle_operation(test_operation, 2, 3, verbose=False)
        
        # Vérifier le résultat
        self.assertEqual(result, 5)

    @patch('cpu_throttler.wait_for_cpu_and_load_availability')
    def test_throttle_operation_throttle_enabled(self, mock_wait):
        # Tester throttle_operation lorsque le throttling est activé
        cpu_throttler.THROTTLE_DISABLE = False
        
        # Définir une opération de test
        def test_operation(x, y):
            return x * y
        
        # Appeler throttle_operation
        result = cpu_throttler.throttle_operation(test_operation, 4, 5, verbose=False)
        
        # Vérifier que wait_for_cpu_and_load_availability a été appelé
        mock_wait.assert_called_once_with(
            cpu_throttler.CPU_THRESHOLD,
            cpu_throttler.LOAD_AVG_THRESHOLD,
            cpu_throttler.CHECK_INTERVAL,
            cpu_throttler.MAX_WAIT_TIME,
            False
        )
        
        # Vérifier le résultat
        self.assertEqual(result, 20)

    def test_environment_variable_configuration(self):
        # Tester la configuration via des variables d'environnement
        # Sauvegarder les valeurs originales
        original_cpu_threshold = cpu_throttler.CPU_THRESHOLD
        original_load_avg_threshold = cpu_throttler.LOAD_AVG_THRESHOLD
        
        # Définir des variables d'environnement
        os.environ['CPU_THRESHOLD'] = '85.0'
        os.environ['LOAD_AVG_THRESHOLD'] = '5.5'
        
        # Recharger le module pour prendre en compte les nouvelles variables d'environnement
        import importlib
        importlib.reload(cpu_throttler)
        
        # Vérifier que les valeurs ont été mises à jour
        self.assertEqual(cpu_throttler.CPU_THRESHOLD, 85.0)
        self.assertEqual(cpu_throttler.LOAD_AVG_THRESHOLD, 5.5)
        
        # Restaurer les valeurs originales
        cpu_throttler.CPU_THRESHOLD = original_cpu_threshold
        cpu_throttler.LOAD_AVG_THRESHOLD = original_load_avg_threshold

    def test_throttle_disable_environment_variable(self):
        # Tester la variable d'environnement THROTTLE_DISABLE
        # Sauvegarder la valeur originale
        original_throttle_disable = cpu_throttler.THROTTLE_DISABLE
        
        # Définir la variable d'environnement
        os.environ['THROTTLE_DISABLE'] = 'true'
        
        # Recharger le module pour prendre en compte la nouvelle variable d'environnement
        import importlib
        importlib.reload(cpu_throttler)
        
        # Vérifier que le throttling est désactivé
        self.assertTrue(cpu_throttler.THROTTLE_DISABLE)
        
        # Restaurer la valeur originale
        cpu_throttler.THROTTLE_DISABLE = original_throttle_disable


if __name__ == '__main__':
    unittest.main()
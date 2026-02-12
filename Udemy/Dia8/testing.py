import unittest
import cambia_texto

class ProbarCambiaTexto(unittest.TestCase):

     def test_mayusculas(self):
         palabra = 'buen dia' #un ejemplo
         resultado = cambia_texto.todo_mayusculas(palabra) # como deberia quedar
         self.assertEqual(resultado, 'BpEN DIA') #chequa el resultado esperado con el obtenido

if __name__ == '__main__':
    unittest.main()


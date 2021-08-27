# Singleton for flags

class Single:
    __instance__ = None

    @staticmethod
    def get_instance():
        """
        Método para acessar a classe estáticamente
        A classe será instanciada apenas uma vez durante toda a execução
        :param: void
        :return: Single
        """
        if Single.__instance__ is None:
            Single.__instance__ = Single()
        return Single.__instance__

    def __init__(self):
        """ Construtor Privado """
        self.route = 'Home'
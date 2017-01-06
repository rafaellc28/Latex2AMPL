class Utils:
    @staticmethod
    def _deleteEmpty(str):
        return str != ""

    @staticmethod
    def _getInt(val):
        if val.replace('.','',1).isdigit():
            val = str(int(float(val)))

        return val

    @staticmethod
    def _isInstanceOfList(obj):
    	return isinstance(obj, list)

    @staticmethod
    def _isInstanceOfStr(obj):
    	return isinstance(obj, str)

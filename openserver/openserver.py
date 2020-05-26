import win32com.client


class OpenServer:
    def __init__(self):
        self.status = "Disconnected"
        self.server = None

    def connect(self):
        """
        Method used to connect to the Petroleum Experts com object which also checks out the license
        """
        self.server = win32com.client.Dispatch("PX32.OpenServer.1")
        self.status = "Connected"
        return print("OpenServer is connected")

    def disconnect(self):
        """
        Method to check in the license
        """
        self.server = None
        self.status = "Disconnected"
        return print("OpenServer has been disconnected")

    def DoCmd(self, Cmd):
        """
        The DoCmd function is used to perform calculations and other functions such as file
        opening and saving in the PETEX programs.

        Arguments:
            Cmd {string} -- OpenServer access string
        """
        if not self.status == 'Connected':
            self.connect()
        try:
            Err = self.server.DoCommand(Cmd)
            if Err > 0:
                print(self.server.GetErrorDescription(Err))
        except:
            self.disconnect()

    def DoSet(self, Sv, Val):
        """
        The DoSet command is used to set the value of a data item

        Arguments:
            Sv {string} -- OpenServer access string
            Val {} -- Value
        """
        if not self.status == 'Connected':
            self.connect()
        try:
            Err = self.server.SetValue(Sv, Val)
            AppName = self.GetAppName(Sv)
            Err = self.server.GetLastError(AppName)
            if Err > 0:
                print(self.server.GetErrorDescription(Err))
        except:
            self.disconnect()

    def DoGet(self, Gv):
        """
        The DoGet function is used to get the value of a data item or result

        Arguments:
            Gv {string} -- OpenServer access string

        Returns:
            Value of a data item or result
        """
        if not self.status == 'Connected':
            self.connect()
        try:
            value = self.server.GetValue(Gv)
            AppName = self.GetAppName(Gv)
            Err = self.server.GetLastError(AppName)
            if Err > 0:
                print(self.server.GetLastErrorMessage(AppName))
            if value.isdigit():  # Checking if integer
                value = int(value)
            else:
                try:
                    value = float(value)  # Checking if float
                except ValueError:
                    pass  # Fallback to string
            return value
        except:
            self.disconnect()

    def GetAppName(self, Strval):
        AppName = Strval.split('.')[0]
        if AppName not in ['PROSPER', 'MBAL', 'GAP', 'PVT', 'RESOLVE']:
            print('Unrecognised application name in tag string')
        return AppName


def DoCmd(Cmd):
    global _petex
    if not '_petex' in globals():
        _petex = OpenServer()
    _petex.DoCmd(Cmd)


def DoSet(Sv, Val):
    global _petex
    if not '_petex' in globals():
        _petex = OpenServer()
    _petex.DoSet(Sv, Val)


def DoGet(Gv):
    global _petex
    if not '_petex' in globals():
        _petex = OpenServer()
    _petex.DoGet(Gv)


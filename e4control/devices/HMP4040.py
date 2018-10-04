# -*- coding: utf-8 -*-

from .device import Device


class HMP4040(Device):

    def __init__(self, connection_type, host, port):
        super(HMP4040, self).__init__(connection_type=connection_type, host=host, port=port)

    def userCmd(self, cmd):
        print('user cmd: %s' % cmd)
        return self.ask(cmd)

    def initialize(self):
        pass

    #Global power (=OUTPUT button on PS)
    def enablePower(self, bValue):
        self.write('OUTP:GEN %i' % bValue)

    def getEnablePower(self):
        return self.ask('OUTP:GEN?') == '1'

    #Output for individual channels
    def enableOutput(self, iOutput, bValue):
        self.write('INST OUT%i' % iOutput)
        self.write('OUTP %i' % bValue)

    def getEnableOutput(self, iOutput):
        self.write('INST OUT%i' % iOutput)
        return self.ask('OUTP?')

    #Over voltage protection
    def setVoltageLimit(self, iOutput, fValue):
        self.write('INST OUT%i' % iOutput)
        self.write('VOLT:PROT %f' % fValue)

    def getVoltageLimit(self, iOutput):
        self.write('INST OUT%i' % iOutput)
        return float(self.ask('VOLT:PROT?'))

    #Nominal voltage to apply
    def setVoltage(self, iOutput, fValue):
        self.write('INST OUT%i' % iOutput)
        self.write('VOLT %f' % fValue)

    def getVoltage(self, iOutput):
        self.write('INST OUT%i' % iOutput)
        return float(self.ask('VOLT?'))

    def measVoltage(self, iOutput):
        self.write('INST OUT%i' % iOutput)
        return float(self.ask('MEAS:VOLT?'))

    #Current (limit)
    def setCurrent(self, iOutput, fValue):
        self.write('INST OUT%i' % iOutput)
        self.write('CURR %f' % fValue)

    def getCurrent(self, iOutput):
        self.write('INST OUT%i' % iOutput)
        return float(self.ask('CURR?'))

    def measCurrent(self, iOutput):
        self.write('INST OUT%i' % iOutput)
        return float(self.ask('MEAS:CURR?'))


    def output(self, show=True):
        sValues = []
        sHeader = []
        isOn = self.getEnablePower()
        if show:
            if isOn:
                print('HMP4040:\t' + '\033[32m ON \033[0m')
            else:
                print('HMP4040:\t' + '\033[31m OFF \033[0m')
        ch = 1
        while ch <= 4:
            outp = self.getEnableOutput(ch)
            v = self.getVoltage(ch)
            vmeas = self.measVoltage(ch)
            i = self.getCurrent(ch)
            imeas = self.measCurrent(ch)

            sValues.append(str(outp))
            sHeader.append('CH%i' % ch)
            sValues.append(str(v))
            sHeader.append('U%i[V]' % ch)
            sValues.append(str(vmeas))
            sHeader.append('Umeas%i[V]' % ch)
            sValues.append(str(i))
            sHeader.append('I%i[V]' % ch)
            sValues.append(str(imeas))
            sHeader.append('Imeas%i[V]' % ch)

            if show:
                if outp == '1':
                    print('CH %i:' % ch + '\t' + '\033[32m ON \033[0m')
                else:
                    print('CH %i:' % ch + '\t' + '\033[31m OFF \033[0m')
                print('Vmeas(set) = %0.3f(%0.3f)V' % (vmeas, v) + '\t' + 'Imeas(set) = %0.4f(%0.4f)A' % (imeas, i))

            ch += 1
        return([sHeader, sValues])

    def interaction(self):
        sChannel = raw_input('Choose channel! \n')
        while sChannel != '1' and sChannel != '2' and sChannel != '3' and sChannel != '4':
            sChannel = raw_input('Possible Channels: 1,2,3 or 4! \n')
        iChannel = int(sChannel)
        print('1: enable Output')
        print('2: set Voltage')
        print('3: set Current')
        x = raw_input('Number? \n')
        while x != '1' and x != '2' and x != '3':
            x = raw_input('Possible Inputs: 1,2 or 3! \n')
        if x == '1':
            bO = raw_input('Please enter ON or OFF! \n')
            if bO == 'ON' or bO == 'on':
                self.enableOutput(iChannel, True)
            elif bO == 'OFF' or bO == 'off':
                self.enableOutput(iChannel, False)
            else:
                pass
        elif x == '2':
            sVoltage = raw_input('Please enter new Voltage in V for CH %i\n' % iChannel)
            self.setVoltage(iChannel, float(sVoltage))
        elif x == '3':
            sCurrent = raw_input('Please enter new Current in A for CH %i\n' % iChannel)
            self.setCurrent(iChannel, float(sCurrent))

BEST_GUESSES = [-0.1, -0.01, 0.01,  0.1]  #LIST OF Possible RATES for calculating IRRs (list of guesses)
SMALL = 0.00000001  #small value - used not to devide by zero

class CashFlows():
    """class holds info about cashflow and calculats NPV and IRR"""
    def __init__(self, cashflows, iteration_no=None, simulation_no=None):
        """@cashflows - list of cashflow values
           @npvs - dict with calcultaned npv with different rates
           @pv - list of present values of cashflow
        """
        self.cashflows = cashflows
        self.npvs = {}
        self.pv = []
        self.iteration_no = iteration_no
        self.simulation_no = simulation_no
        self.zerodivisionerror = False

    def derivativeNpv(self,  rate):
        """calculate derivative npv"""
        total = 0.0
        rate_plus_1 = 1 + rate
        cf = self.cashflows[1:]  #copy of CF except first value for calc derivative
        for i, cashflow in enumerate(cf):
            val = (-1 * (i) * cashflow / (rate_plus_1** (i + 1)+SMALL))
            total += val
        return total

    def npv(self,  rate, save_pv=False):
        """Calculation on NPV based on given @rate"""
        if rate not in self.npvs:
            total = 0.0
            rate_plus_1 = 1 + rate
            for i, cashflow in enumerate(self.cashflows):
                stepen = (i)
                small = SMALL if i > 0 else 0  #small value - not to devide by zero
                val = (cashflow / ((rate_plus_1)** (stepen) + small))
                total += val
                if save_pv:  #if @save_pv
                    self.pv.append(val)

            self.npvs[rate] = total  #saving in dict because it is heavy calculations
            return total
        else:
            return  self.npvs[rate]  #load from dict, if it was already calculated

    def improve(self,  guess):
        """Tries to improve last guess"""
        derivative = self.derivativeNpv(guess)
        if derivative == 0:
            if not self.zerodivisionerror:
                msg = "\nJust info: ZeroDivisionError while NPV calculation" \
                      "Details in report: simulation = %s, iteration = %s" \
                      % (self.simulation_no, self.iteration_no)
                print msg
                self.zerodivisionerror = True
            derivative = 0.0001
        result = guess - self.npv(guess) / derivative
        if abs(result) < 2:
            return result

    def goodEnough(self,  guess):
        """Finding when NPV is near to zero, is abs < 0.1"""
        return (abs(self.npv(guess)) <= 0.1)  #return True if NPV is near to zero (-0.1--0.1)

    def findIrrNewton(self, guess):
        """Finding IRR using Newton method with limited number of iterations =50"""
        stop = self.goodEnough(guess)  #when we should stop improving our guesses
        iter_no = 0
        while (not stop):
            iter_no += 1
            guess = self.improve(guess)  #try to find better guess or IRR
            if guess  != None:
                stop = self.goodEnough(guess)  #is guess good enough?
            else:
                stop = True
            if iter_no > 50:  #stop if we have more than 50 iterations - means this guess is wrong
                guess = None
                stop = True
        return guess

    def get_one_irr(self,  irrs):
        """Input: list of irrs
        return  most logical irr
        """
        for irr in irrs:
            if irr is  None:
                continue
            if irr > 0.001 and irr <0.99:
                return irr
            if irr > -0.99 and irr < -0.001:
                return irr
            if irr > - 0.001 and irr < 0.001:
                return irr
            if irr < - 0.99:
                return irr
        return irr

    def getPossibleIrrs(self):
        """return  list of possible irrs using different guesses from setup"""
        irrs = []
        for guess_rate in BEST_GUESSES: #finding irr using newthon method for each guess in best guesses
            irr = self.findIrrNewton(guess_rate)  #founded IRR
            irrs.append(irr)  #appending it to list of results
        return irrs

    def irr(self):
        """Calculates multiple irrs using guesses, returns most logical one"""
        irrs = self.getPossibleIrrs()  #getting all irr results
        irrs.sort(reverse=True)  #sort them
        return  self.get_one_irr(irrs)  #find one - most logical, because any equ can have multiple roots


def npvPv(rate, vals):
    """return  NPV value and list of PV"""
    c = CashFlows(vals)
    return (c.npv(rate, save_pv=True), c.pv)

if __name__ == '__main__':
    #SMALL TESTS
    vals = [-52500.0, 9.094947017729282e-13, -3000.000000000002, -1999.9999999999986, 10312.917080295065, -4554.1354255383039, -5105.5779770375266, 7002.2624291253878, 5634.9137524801899, 6215.0637694091101, 5451.4289039946689, 2496.5823558127327, 3978.1215116621293, 3540.2299623837584, 3206.7971105880242, 3016.1425272861957, 4780.0596139307872, 5336.239675863193, 7117.5060421685785, 6900.6579751536447, 5691.1671272720478, 8703.9073283371126, 5285.9878539342035, -416.6339909854961, 6653.8555931863211, 5669.0730892146212, 4914.0290583622036, 5548.3829570661155, 7969.833817518077, 7691.1232862130501, 10274.188320124791, 11946.028667951214, 8519.0887947056854, 9529.3109333959637, 9071.4027094270241, -735.08515308104836, 6710.0208204081546, 5750.6354532294908, 4871.0665364767683, 5917.3624066550865, 7312.345421327992, 8451.4701351231633, 11015.196071144206, 11334.545811574646, 9174.6162399457207, 9748.8235396951204, 9375.9967489622068, -307.50607637522796, 6705.7745237545805, 5663.062778287971, 5547.1303219264328, 4714.3538518292653, 7393.1541563399796, 9233.9995980640015, 10638.039945775592, 10096.774458680329, 9765.6144568849359, 9939.2905421443793, 8959.2510035102878, -503.41361386985159, 6730.4035665583369, 5347.360198277388, 5362.9887293777319, 5490.1159633674579, 7207.1527733107469, 8697.1514895566888, 11460.744856578127, 10128.123442041939, 8562.6784699011259, 10983.378495895653, 9859.1028149740177, -781.86115991419399, 6622.042841081312, 5232.4035403778298, 5248.4570476110603, 6052.3091183943043, 6934.1220330320084, 9012.4142354032301, 11841.675380078836, 9486.0370643950828, 10252.473621029467, 10310.64517414683, 9434.3955935036247, 46.123073375468152, 6806.8082467515542, 5769.0595844708041, 5174.7667732016271, 6716.5759906468575, 7434.9062466735195, 8643.1268179751005, 13632.927694774904, 10778.867890635292, 8409.8470366867605, 12021.822806167367, 10601.465386621025, -962.14694396295442, 6962.3082957340612, 5295.4571627679979, 5976.2390296886324, 6244.8155147842144, 7666.8695054020282, 8295.3207165046988, 11742.055766048079, 13313.334722960093, 9015.6984657350386, 10314.2475292411, 10165.310980490749, -664.40049197974827, 7773.294586336503, 6008.6692472765089, 5600.2217423336233, 5492.5680989610355, 8697.8936226116857, 8569.2770641057232, 12017.957509182392, 12148.197320661924, 9112.0083209206859, 11181.596206223838, 10317.954937037633, -364.92484626579113, 7504.9517987759973, 5704.9963507485318, 5790.4446962159427, 6499.1038574446511, 8229.267682323878, 8036.0316875122326, 12283.209741605489, 13049.353101204457, 9048.5477859057701, 10775.260838053206, 10410.861587470185, -703.12404105089581, 7430.2997042469788, 5801.9408283786197, 5668.301590239259, 6683.3416712388316, 7989.6964873877387, 10281.587628510635, 11248.798025614402, 12095.30774515239, 10389.636384907648, 11658.157316488572, 11114.352821420869, -1118.7518386910247, 7263.4760424815522, 5678.8369965810371, 7087.8664264264462, 5411.0809770516889, 8609.0646933039552, 10459.442466664432, 13042.209104422544, 11240.852467487228, 10908.025276886472, 12699.735188558565, 10315.737752453093, -1174.1444948088933, 7506.4961734529152, 6185.6166090621655, 5192.6365718888774, 7071.8520606767252, 9023.5819129335487, 8280.4872561192024, 13729.626119623648, 11073.496823111362, 10697.57968316798, 10460.807867587966, 11465.634442825783, -714.48340436391584, 4686.921162846289, 4131.1039002659536, 4786.7749632913137, 4382.6823891166432, 5706.93630069746, 7431.2204186033914, 8509.8075906323302, 9110.5269952439721, 8139.361443169204, 8356.5720976058292, 7632.446026610216, -555.14693166405777, 5611.6749463672541, 4402.2292765757002, 4311.6860213645168, 4651.7191294300655, 6073.3878282425349, 6222.6813321364461, 10256.585821178143, 9180.3196616838868, 6712.7862142481672, 8951.0122879210539, 7945.1097895652128, -863.37691291227566, 5559.043961319604, 4640.2558328986033, 3925.1673153095708, 4400.8805809087216, 6427.1633906306943, 6279.1318435972735, 10219.876135870192, 8450.7614839756552, 7300.5816429141823, 9094.0630577289849, 8167.1729693360285, -706.47668455910116, 5530.9096311506264, 4429.8794235583255, 4461.6003525139031, 5180.3331092140088, 5731.1588299356899, 7355.1554856490475, 8932.2570346145967, 10547.076753181906, 7707.3944135819002, 8445.2136283408599, 8905.466038860257, -1123.6937954504911, 5708.4922088313488, 4858.9782361956322, 4628.2308463017944, 4967.958025068654, 6468.9141773962328, 7617.2468741553275, 10090.369807591378, 9719.4358014486425, 8246.9393376979842, 9489.720838223293, 8261.5879209848863, -1065.9991467367872, 6275.1010199424354, 4410.6724305425287, 5121.2548832872135, 4964.9849173432667, 5974.2281760169153, 7898.8334953196791, 10668.799142429123, 8956.3175131871394, 8794.0810666176167, 9280.5169997192261, 7943.242486161138, -793.70537807980236, 5704.8219367140337, 4910.2258162493745, 5140.5154933015619, 5109.001813561923, 6634.9976013057221, 7422.8494847777511, 10844.986359943065, 9784.9421698982696, 8500.2204746230418, 10257.702603048754, 7526.0237508893661, -1046.8078115980661, 6617.9684016175443, 5001.1188275615395, 5117.0229527069478, 5305.6455985498542, 6965.7356269573738, 7823.7712315417357, 10346.949318598427, 11128.869958660265, 9400.2822001810018, 8737.6186644093323, 9087.8949768541061, -508.85982122375208, 6078.9761817095368, 5127.3951217802523, 4741.5478660529698, 5458.1467111769543, 7969.4766495295771, 6374.5075125167023, 11239.692393848965, 11299.001627192769, 8461.1299277465478, 9652.866022894199, 8795.2223602662616, -1006.3893133863476, 6877.7655485983714, 5254.7633672579705, 4912.6929833628456, 4890.6393602096159, 7640.5366598476012, 8883.7146295852035, 10800.232901625091, 9930.7375283106085, 10133.989817086498, 10166.763140080729, 8883.0221999942405, -722.62381516753885, 6694.0034341773007, 5337.9301467509467, 5128.3419748295873, 5530.7490062188936, 7750.761308764324, 8434.9019245882373, 11747.22917231989, 10749.223044332512, 9477.1238541874245, 10872.153426920808, 9489.7554319245719, -919.67147347397167, 6995.6239901504996, 5766.0148261194881, 5254.8960215442485, 5321.9538629097588, 8011.0884056396899, 8186.4395813027641, 11262.613464218692, 11782.9308645906, 10150.715372268964, 10236.620797254944, 8929.1086940157147, -447.6888474397856, 7700.4797428236407, 5733.42060891445, 4487.978485906855, 6641.6643363952262, 8011.2957939433927, 7907.4645001282915, 12162.110345826683, 11203.783303928196, 10122.85228786607, 10059.847222695551, 10400.669900191055, -408.03959613845291, 6594.9943009343278, 5123.4874257404072, 5648.5223072312128, 5378.8995762653431, 8468.7265398993641, 7859.8950803189018, 12676.466433045503, 11108.682010216446, 8927.8342236975004, 11860.12163110762, 10047.776191492478, -1397.981258339747, 7331.3980754192944, 5290.6318374881248, 6146.0057459494901, 5913.2340178056511, 8399.7238174893719, 8345.0268933752341, 11510.66897625773, 13282.209440672035, 10042.929883737481, 11355.622122722163, 9771.1708978037368, -1464.556666966484, 7830.6010939082726, 5012.5153578713634, 5764.9824408538516, 7588.017818553928, 6273.3250461460866, 8907.4593727349275, 12630.011774394825, 12396.754794301227, 11115.033883777502, 10471.32094304479, 10100.458264748399, -514.3024749248234]
    c = CashFlows(vals)
    print c.irr()

    vals = [-75000, 25000, 25000, 25000, 25000, 25000, -10000]
    c = CashFlows(vals)
    print c.irr()
    c.npv(0.111, save_pv=True)
    print c.pv


    vals =[-135058400,-540178600,64463724.54,97045495.07,100783477.3,100968948.1,104441595,103025235.5,105645724.4,106890037.3,106759758.9,112114108.4,109985990.7,111547302.2,108697197.9,80079613.2,80517564.03,80579860.25,84190124.97,85843711.75,88112482.16,88717774.7,90455694.38,92140853.72,95184714.12]
    c = CashFlows(vals)
    print c.irr()


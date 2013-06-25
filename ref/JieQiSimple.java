/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.tq.divination;

/**
 *
 * @author thule
 */
public class JieQiSimple extends AbstractJieQi {

    @Override
    public boolean getJieqiTime(int year, int index, int[] cal) {
        double jd, q;
        if ((index < 0) || (index > JIEQI24.length)) {
            return false;
        }
        jd = 365.2422 * (year - 2000);
        q = jiaoCal(jd + index * 15.2, (index - 3) * 15) + 8.0/24 + J2000;
        setFromJD(q, true, cal);
        return true;
    }

    @Override
    public boolean getJieqiTimes(int year, int start_index, int count, int[][] cal) {
        double jd, q;
        if ((start_index < 0) || (start_index > JIEQI24.length)) {
            return false;
        }
        if (count < 0) {
            return false;
        }
        jd = 365.2422 * (year - 2000);
        for(int i = 0; i < count; i++) {
            q = jiaoCal(jd + i * 15.2, (i - 3) * 15) + 8.0/24 + J2000;
            setFromJD(q, true, cal[i]);
        }
        return true;
    }

    @Override
    public boolean getJieqiIndex(int[] cal, int[] time) {
        int year, i, j;
        double[] q=new double[2];
        double jd;
        int[] cal2=new int[6];
        year = cal[0];
        if ((cal[1] <= 0) || (cal[1] >12)) {
            return false;
        }
        if ((cal[2] <= 0) || (cal[2]>31)) {
            return false;
        }
        switch (cal[1]) {
            case 1:
                i = 22;
                year--;
                break;
            default:
                i = (cal[1] - 2) * 2;
                break;
        }
        jd = 365.2422 * (year - 2000);
        for(j = 0; j < q.length; j++) {
            q[j] = jiaoCal(jd + (i + j) * 15.2, (i + j - 3) * 15) + 8.0/24 + J2000;
        }

        j = 0;
        setFromJD(q[0], true, cal2);
        for(int k = 2; k < cal2.length; k++) {
            if(cal2[k] > cal[k]) {
                j = 1;
                time[0] = year;
                time[1] = i - 1;
                if(time[1] <= 0) {
                    time[1] += 24;
                    time[0]--;
                }
                break;
            } else if(cal2[k] < cal[k]) {
                break;
            }
        }

        if (1 != j) {
            setFromJD(q[1], true, cal2);
            for (int k = 2; k < cal2.length; k++) {
                if (cal2[k] > cal[k]) {
                    j = 1;
                    time[0] = year;
                    time[1] = i;
                    break;
                } else if(cal2[k] < cal[k]) {
                    break;
                }
            }
            if (1 != j) {
                time[0] = year;
                time[1] = i + 1;
            }
        }

        return true;
    }

    private static final double J2000 = 2451545;
    private static final double rad = 180 * 3600 / Math.PI;
    private static final double RAD = 180 / Math.PI;
    private static final double[] nutB = new double[]{2.1824391966, -33.757045954, 0.0000362262, 3.7340E-08, -2.8793E-10, -171996, -1742, 92025, 89,
        3.5069406862, 1256.663930738, 0.0000105845, 6.9813E-10, -2.2815E-10, -13187, -16, 5736, -31,
        1.3375032491, 16799.418221925, -0.0000511866, 6.4626E-08, -5.3543E-10, -2274, -2, 977, -5,
        4.3648783932, -67.514091907, 0.0000724525, 7.4681E-08, -5.7586E-10, 2062, 2, -895, 5,
        0.0431251803, -628.301955171, 0.0000026820, 6.5935E-10, 5.5705E-11, -1426, 34, 54, -1,
        2.3555557435, 8328.691425719, 0.0001545547, 2.5033E-07, -1.1863E-09, 712, 1, -7, 0,
        3.4638155059, 1884.965885909, 0.0000079025, 3.8785E-11, -2.8386E-10, -517, 12, 224, -6,
        5.4382493597, 16833.175267879, -0.0000874129, 2.7285E-08, -2.4750E-10, -386, -4, 200, 0,
        3.6930589926, 25128.109647645, 0.0001033681, 3.1496E-07, -1.7218E-09, -301, 0, 129, -1,
        3.5500658664, 628.361975567, 0.0000132664, 1.3575E-09, -1.7245E-10, 217, -5, -95, 3};
    private static final double[] GXC_e = new double[]{0.016708634, -0.000042037, -0.0000001267};
    private static final double[] GXC_p = new double[]{102.93735 / RAD, 1.71946 / RAD, 0.00046 / RAD};
    private static final double[] GXC_l = new double[]{280.4664567 / RAD, 36000.76982779 / RAD, 0.0003032028 / RAD, 1 / 49931000 / RAD, -1 / 153000000 / RAD};
    private static final double GXC_k=20.49552 / rad;
    private static final double[] E10 = new double[]{
        1.75347045673, 0.00000000000, 0.0000000000, 0.03341656456, 4.66925680417, 6283.0758499914, 0.00034894275, 4.62610241759, 12566.1516999828, 0.00003417571, 2.82886579606, 3.5231183490,
        0.00003497056, 2.74411800971, 5753.3848848968, 0.00003135896, 3.62767041758, 77713.7714681205, 0.00002676218, 4.41808351397, 7860.4193924392, 0.00002342687, 6.13516237631, 3930.2096962196,
        0.00001273166, 2.03709655772, 529.6909650946, 0.00001324292, 0.74246356352, 11506.7697697936, 0.00000901855, 2.04505443513, 26.2983197998, 0.00001199167, 1.10962944315, 1577.3435424478,
        0.00000857223, 3.50849156957, 398.1490034082, 0.00000779786, 1.17882652114, 5223.6939198022, 0.00000990250, 5.23268129594, 5884.9268465832, 0.00000753141, 2.53339053818, 5507.5532386674,
        0.00000505264, 4.58292563052, 18849.2275499742, 0.00000492379, 4.20506639861, 775.5226113240, 0.00000356655, 2.91954116867, 0.0673103028, 0.00000284125, 1.89869034186, 796.2980068164,
        0.00000242810, 0.34481140906, 5486.7778431750, 0.00000317087, 5.84901952218, 11790.6290886588, 0.00000271039, 0.31488607649, 10977.0788046990, 0.00000206160, 4.80646606059, 2544.3144198834,
        0.00000205385, 1.86947813692, 5573.1428014331, 0.00000202261, 2.45767795458, 6069.7767545534, 0.00000126184, 1.08302630210, 20.7753954924, 0.00000155516, 0.83306073807, 213.2990954380,
        0.00000115132, 0.64544911683, 0.9803210682, 0.00000102851, 0.63599846727, 4694.0029547076, 0.00000101724, 4.26679821365, 7.1135470008, 0.00000099206, 6.20992940258, 2146.1654164752,
        0.00000132212, 3.41118275555, 2942.4634232916, 0.00000097607, 0.68101272270, 155.4203994342, 0.00000085128, 1.29870743025, 6275.9623029906, 0.00000074651, 1.75508916159, 5088.6288397668,
        0.00000101895, 0.97569221824, 15720.8387848784, 0.00000084711, 3.67080093025, 71430.6956181291, 0.00000073547, 4.67926565481, 801.8209311238, 0.00000073874, 3.50319443167, 3154.6870848956,
        0.00000078756, 3.03698313141, 12036.4607348882, 0.00000079637, 1.80791330700, 17260.1546546904, 0.00000085803, 5.98322631256, 161000.6857376741, 0.00000056963, 2.78430398043, 6286.5989683404,
        0.00000061148, 1.81839811024, 7084.8967811152, 0.00000069627, 0.83297596966, 9437.7629348870, 0.00000056116, 4.38694880779, 14143.4952424306, 0.00000062449, 3.97763880587, 8827.3902698748,
        0.00000051145, 0.28306864501, 5856.4776591154, 0.00000055577, 3.47006009062, 6279.5527316424, 0.00000041036, 5.36817351402, 8429.2412664666, 0.00000051605, 1.33282746983, 1748.0164130670,
        0.00000051992, 0.18914945834, 12139.5535091068, 0.00000049000, 0.48735065033, 1194.4470102246, 0.00000039200, 6.16832995016, 10447.3878396044, 0.00000035566, 1.77597314691, 6812.7668150860,
        0.00000036770, 6.04133859347, 10213.2855462110, 0.00000036596, 2.56955238628, 1059.3819301892, 0.00000033291, 0.59309499459, 17789.8456197850, 0.00000035954, 1.70876111898, 2352.8661537718};
    private static final double[] E11 = new double[]{
        6283.31966747491, 0.00000000000, 0.0000000000, 0.00206058863, 2.67823455584, 6283.0758499914, 0.00004303430, 2.63512650414, 12566.1516999828, 0.00000425264, 1.59046980729, 3.5231183490,
        0.00000108977, 2.96618001993, 1577.3435424478, 0.00000093478, 2.59212835365, 18849.2275499742, 0.00000119261, 5.79557487799, 26.2983197998, 0.00000072122, 1.13846158196, 529.6909650946,
        0.00000067768, 1.87472304791, 398.1490034082, 0.00000067327, 4.40918235168, 5507.5532386674, 0.00000059027, 2.88797038460, 5223.6939198022, 0.00000055976, 2.17471680261, 155.4203994342,
        0.00000045407, 0.39803079805, 796.2980068164, 0.00000036369, 0.46624739835, 775.5226113240, 0.00000028958, 2.64707383882, 7.1135470008, 0.00000019097, 1.84628332577, 5486.7778431750,
        0.00000020844, 5.34138275149, 0.9803210682, 0.00000018508, 4.96855124577, 213.2990954380, 0.00000016233, 0.03216483047, 2544.3144198834, 0.00000017293, 2.99116864949, 6275.9623029906};
    private static final double[] E12 = new double[]{
        0.00052918870, 0.00000000000, 0.0000000000, 0.00008719837, 1.07209665242, 6283.0758499914, 0.00000309125, 0.86728818832, 12566.1516999828, 0.00000027339, 0.05297871691, 3.5231183490,
        0.00000016334, 5.18826691036, 26.2983197998, 0.00000015752, 3.68457889430, 155.4203994342, 0.00000009541, 0.75742297675, 18849.2275499742, 0.00000008937, 2.05705419118, 77713.7714681205,
        0.00000006952, 0.82673305410, 775.5226113240, 0.00000005064, 4.66284525271, 1577.3435424478};
    private static final double[] E13 = new double[]{0.00000289226, 5.84384198723, 6283.0758499914, 0.00000034955, 0.00000000000, 0.0000000000, 0.00000016819, 5.48766912348, 12566.1516999828};
    private static final double[] E14 = new double[]{0.00000114084, 3.14159265359, 0.0000000000, 0.00000007717, 4.13446589358, 6283.0758499914, 0.00000000765, 3.83803776214, 12566.1516999828};
    private static final double[] E15 = new double[]{0.00000000878, 3.14159265359, 0.0000000000};
    private static final double[] E20 = new double[]{
        0.00000279620, 3.19870156017, 84334.6615813083, 0.00000101643, 5.42248619256, 5507.5532386674, 0.00000080445, 3.88013204458, 5223.6939198022, 0.00000043806, 3.70444689758, 2352.8661537718,
        0.00000031933, 4.00026369781, 1577.3435424478, 0.00000022724, 3.98473831560, 1047.7473117547, 0.00000016392, 3.56456119782, 5856.4776591154, 0.00000018141, 4.98367470263, 6283.0758499914,
        0.00000014443, 3.70275614914, 9437.7629348870, 0.00000014304, 3.41117857525, 10213.2855462110};
    private static final double[] E21 = new double[]{0.00000009030, 3.89729061890, 5507.5532386674, 0.00000006177, 1.73038850355, 5223.6939198022};
    private static final double[] E30 = new double[]{
        1.00013988799, 0.00000000000, 0.0000000000, 0.01670699626, 3.09846350771, 6283.0758499914, 0.00013956023, 3.05524609620, 12566.1516999828, 0.00003083720, 5.19846674381, 77713.7714681205,
        0.00001628461, 1.17387749012, 5753.3848848968, 0.00001575568, 2.84685245825, 7860.4193924392, 0.00000924799, 5.45292234084, 11506.7697697936, 0.00000542444, 4.56409149777, 3930.2096962196};
    private static final double[] E31 = new double[]{0.00103018608, 1.10748969588, 6283.0758499914, 0.00001721238, 1.06442301418, 12566.1516999828, 0.00000702215, 3.14159265359, 0.0000000000};
    private static final double[] E32 = new double[]{0.00004359385, 5.78455133738, 6283.0758499914};
    private static final double[] E33 = new double[]{0.00000144595, 4.27319435148, 6283.0758499914};
    private static final double[] dts = new double[]{
   -4000,108371.7,-13036.80,392.000, 0.0000, -500, 17201.0,  -627.82, 16.170,-0.3413,
    -150, 12200.6,  -346.41,  5.403,-0.1593,  150,  9113.8,  -328.13, -1.647, 0.0377,
     500,  5707.5,  -391.41,  0.915, 0.3145,  900,  2203.4,  -283.45, 13.034,-0.1778,
    1300,   490.1,   -57.35,  2.085,-0.0072, 1600,   120.0,    -9.81, -1.532, 0.1403,
    1700,    10.2,    -0.91,  0.510,-0.0370, 1800,    13.4,    -0.72,  0.202,-0.0193,
    1830,     7.8,    -1.81,  0.416,-0.0247, 1860,     8.3,    -0.13, -0.406, 0.0292,
    1880,    -5.4,     0.32, -0.183, 0.0173, 1900,    -2.3,     2.06,  0.169,-0.0135,
    1920,    21.2,     1.69, -0.304, 0.0167, 1940,    24.2,     1.22, -0.064, 0.0031,
    1960,    33.2,     0.51,  0.231,-0.0109, 1980,    51.0,     1.29, -0.026, 0.0032,
    2000,    64.7,    -1.66,  5.224,-0.2905, 2150,   279.4,   732.95,429.579, 0.0158, 6000};

    private static int int2(double d) {
        int i=(int)Math.floor(d);
        if(i < 0) {
            i++;
        }
        return i;
    }
    private static double rad2mrad(double lrad) {
        lrad = lrad % (2 * Math.PI);
        if (lrad < 0) {
            lrad += 2 * Math.PI;
        }
        return lrad;
    }

    private static double Enn(double Ennt, double F[]) {
        double v = 0;
        for (int i = 0; i < F.length; i += 3) {
            v += F[i] * Math.cos(F[i + 1] + Ennt * F[i + 2]);
        }
        return v;
    }

    private static void earCal(double jd, double[] llr) {
        double t1, t2, t3, t4, t5;
        t1 = jd / 365250;
        t2 = t1 * t1;
        t3 = t2 * t1;
        t4 = t3 * t1;
        t5 = t4 * t1;
        llr[0] = Enn(t1, E10) + Enn(t1, E11) * t1 + Enn(t1, E12) * t2 + Enn(t1, E13) * t3 + Enn(t1, E14) * t4 + Enn(t1, E15) * t5;
        llr[1] = Enn(t1, E20) + Enn(t1, E21) * t1;
        llr[2] = Enn(t1, E30) + Enn(t1, E31) * t1 + Enn(t1, E32) * t2 + Enn(t1, E33) * t3;
        llr[0] = rad2mrad(llr[0]);
        return;
    }

    private static void addGxc(double t, double[] zb) {
        double t1,t2,t3,t4,l,p,e,dl,dp;
        t1 = t / 36525;
        t2 = t1 * t1;
        t3 = t2 * t1;
        t4 = t3 * t1;
        l = GXC_l[0] + GXC_l[1] * t1 + GXC_l[2] * t2 + GXC_l[3] * t3 + GXC_l[4] * t4;
        p = GXC_p[0] + GXC_p[1] * t1 + GXC_p[2] * t2;
        e = GXC_e[0] + GXC_e[1] * t1 + GXC_e[2] * t2;
        dl = l - zb[0];
        dp = p - zb[0];
        zb[0] -= GXC_k * (Math.cos(dl) - e * Math.cos(dp)) / Math.cos(zb[1]);
        zb[1] -= GXC_k * Math.sin(zb[1]) * (Math.sin(dl) - e * Math.sin(dp));
        zb[0] = rad2mrad(zb[0]);
        return;
    }
    private static void nutation(double t, double[] d) {
        double c,t1,t2,t3,t4;
        t = t / 36525;
        t1 = t;
        t2 = t1 * t1;
        t3 = t2 * t1;
        t4 = t3 * t1;
        for (int i = 0; i<nutB.length; i += 9) {
            c = nutB[i] + nutB[i+1] * t1 + nutB[i+2] * t2 + nutB[i+3] * t3 + nutB[i+4] * t4;
            d[0] += (nutB[i+5] + nutB[i+6] * t / 10) * Math.sin(c);
            d[1] += (nutB[i+7] + nutB[i+8] * t / 10) * Math.cos(c);
        }
        d[0] /= rad * 10000;
        d[1] /= rad * 10000;
        return;
    }
    private static double jiaoCai(double t, double jiao) {
        double[] sun=new double[3];
        double[] d = new double[2];
        earCal(t, sun);
        nutation(t, d);
        sun[0] += Math.PI;
        sun[1] = - sun[1];
        addGxc(t,sun);
        sun[0] += d[0];
        return rad2mrad(jiao - sun[0]);
    }

    private static double jiaoCal(double t, double jiao) {
        double t1,t2,v,v1,v2,k,k2;
        t1 = t;
        t2 = t1 + 360;
        jiao = jiao * Math.PI / 180;
        v1 = jiaoCai(t1, jiao);
        v2 = jiaoCai(t2, jiao);
        if (v1 < v2) {
            v2 -= 2 * Math.PI;
        }
        k = 1;
        for (int i = 0; i < 10; i++) {
            k2 = (v2 - v1) / (t2 - t1);
            if (Math.abs(k2) > 1e-15) {
                k = k2;
            }
            t = t1 - v1 / k;
            v = jiaoCai(t, jiao);
            if (v > 1) {
                v -= 2 * Math.PI;
            }
            if (Math.abs(v) < 1e-8) {
                break;
            }
            t1 = t2;
            v1 = v2;
            t2 = t;
            v2 = v;
        }
        return t;
    }
    private static double deltatT(double jd) {
        double y, v, t1, t2, t3;
        int i;
        y = jd / 365.2425 + 2000;
        for (i = 0; i < dts.length; i += 5) {
            if ((y < dts[i + 5]) || (i == (dts.length - 5))) {
                break;
            }
        }
        t1 = (y - dts[i]) / (dts[i + 5] - dts[i]) * 10;
        t2 = t1 * t1;
        t3 = t2 * t1;
        v = dts[i + 1] + dts[i + 2] * t1 + dts[i + 3] * t2 + dts[i + 4] * t3;
        v = v / 86400.0;
        return v;
    }
    private static void setFromJD(double jd, boolean UTC, int[] cal) {
        double F;
        int A,D;
        if (UTC) {
            jd -= deltatT(jd - J2000);
        }
        jd += 0.5;
        A=int2(jd);
        F = jd - A;
        if(A > 2299161) {
            D = int2((A - 1867216.25) / 36524.25);
            A += 1 + D - int2(D / 4);
        }
        A += 1524;
        cal[0] = int2((A - 122.1) / 365.25);
        D = A - int2(365.25 * cal[0]);
        cal[1] = int2(D / 30.6001);
        cal[2] = D - int2(cal[1]*30.6001);
        cal[0] -= 4716;
        cal[1] --;
        if (cal[1] > 12) {
            cal[1] -= 12;
        }
        if (cal[1] <=2) {
            cal[0]++;
        }
        F *= 24;
        cal[3] = int2(F);
        F -= cal[3];
        F *= 60;
        cal[4] = int2(F);
        F -= cal[4];
        F *= 60;
        cal[5] = (int)Math.floor(F+0.5);
        if(cal[5] >= 60) {
            cal[5] -= 60;
            cal[4] += 1;
        }
        if(cal[4] >= 60) {
            cal[4] -= 60;
            cal[3] += 1;
        }
        return;
    }

}

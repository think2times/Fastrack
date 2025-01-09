from pyspark import SparkConf, SparkContext
import findspark

if __name__ == '__main__':
    findspark.init()
    conf = SparkConf().setAppName('spark').setMaster('local[*]')
    sc = SparkContext(conf=conf)
    sc.setLogLevel("WARN")

    t1 = sc.textFile("F:/Projects/Fastrack/Doing/bd/spark_covid-19")

    def mapT(s):
        line = s.split(",")
        if (len(line) >= 6):
            state = line[2]
            casesStr = line[4]
            deathsStr = line[5]
            cases = int(casesStr if (casesStr and casesStr != '') else '0')
            deaths = int(deathsStr if (deathsStr and deathsStr != '') else '0')
            return (state, (cases, deaths))
        else:
            return None

    t1.filter(lambda s: s and s != '') \
        .map(mapT) \
        .filter(lambda s: s != None) \
        .reduceByKey(lambda v1, v2: (v1[0] + v2[0], v1[1] + v2[1])) \
        .sortByKey(ascending=True, numPartitions=1) \
        .foreach(lambda t: print(t[0] + "  " + str(t[1][0]) + "  " + str(t[1][1])))

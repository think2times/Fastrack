package spark.demo;

/*import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import scala.Tuple2;

import java.util.Arrays;
import java.util.function.Function;

public class JavaWordCount {
    public static void main(String args[]){
        SparkConf conf=new SparkConf();
        conf.setAppName("Spark-JavaWordCount");
        conf.setMaster("spark://centos01:7077");
        JavaSparkContext jsc=new JavaSparkContext(conf);
        JavaRDD<String> linesRDD = jsc.textFile(args[0]);
        JavaRDD<String> wordsRDD = linesRDD.flatMap(x -> Arrays.asList(x.split(" ")).iterator());
        JavaPairRDD<String, Integer> paresRDD = wordsRDD.mapToPair(x -> new Tuple2<String, Integer>(x, 1));
        JavaPairRDD<String, Integer> wordCountsRDD = paresRDD.reduceByKey((x, y) -> x + y);
        wordCountsRDD.saveAsTextFile(args[1]);

    }
}*/

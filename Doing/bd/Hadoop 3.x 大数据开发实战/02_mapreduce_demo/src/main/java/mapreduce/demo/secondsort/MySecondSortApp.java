package mapreduce.demo.secondsort;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import java.io.IOException;

/**
 * MapReduce应用程序主类
 */
public class MySecondSortApp {
    public static void main(String[] args) throws IOException,
            ClassNotFoundException, InterruptedException {

        Configuration conf = new Configuration();
        // 设置HDFS访问路径
        conf.set("fs.default.name", "hdfs://192.168.170.133:9000");
        Job job = Job.getInstance(conf, "MySecondSortApp");
        job.setJarByClass(MySecondSortApp.class);

        // 设置Mapper处理类
        job.setMapperClass(MyMapper.class);
        // 设置自定义分区类
        job.setPartitionerClass(MyPartitioner.class);
        // 设置自定义分组类
        job.setGroupingComparatorClass(MyGroupComparator.class);
        // 设置Reducer处理类
        job.setReducerClass(MyReducer.class);

        // 设置Map任务输出类型，与map()方法输出类型一致
        job.setMapOutputKeyClass(MyKeyPair.class);
        job.setMapOutputValueClass(IntWritable.class);

        // 设置Reduce任务输出类型，与reduce()方法输出类型一致
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        // 将输入的数据集分割成小数据块splites
        job.setInputFormatClass(TextInputFormat.class);
        // 提供一个RecordWriter的实现，负责数据输出
        job.setOutputFormatClass(TextOutputFormat.class);

        // 设置数据在HDFS中的输入和输出目录
        FileInputFormat.addInputPath(job, new Path("/input/"));
        FileOutputFormat.setOutputPath(job, new Path("/output"));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

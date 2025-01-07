package mapreduce.demo.test;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class MyMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    // 重新map()函数
    public void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {
        // 业务逻辑
    }
}

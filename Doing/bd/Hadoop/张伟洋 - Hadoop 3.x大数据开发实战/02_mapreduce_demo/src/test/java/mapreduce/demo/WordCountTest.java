package mapreduce.demo;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mrunit.mapreduce.MapDriver;
import org.junit.Test;

public class WordCountTest {

    @Test
    public void testMapper() throws IOException {
        Text value = new Text("hello hadoop hello java");
        // 由于测试的mapper，所以适用MRUnit的MapDriver
        new MapDriver<Object, Text, Text, IntWritable>()
                // 配置mapper
                .withMapper(new WordCount.TokenizerMapper())
                // 设置输入值
                .withInput(new LongWritable(0), value)
                // 设置期望输出：key和value
                .withOutput(new Text("hello"), new IntWritable(1)).runTest();
    }

}

package mapreduce.demo.secondsort;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;
import java.util.StringTokenizer;

/**
 * 定义Mapper类
 */
public class MyMapper extends Mapper<LongWritable, Text, MyKeyPair, IntWritable> {
    /**
     * 重新map()方法
     */
    public void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {
        String line = value.toString();
        // 将输入的一行数据默认按空格、制表符\t、换行符\n、回车符\r进行分割，也可以加入一个参数指定分隔符
        StringTokenizer itr = new StringTokenizer(line);

        String first = itr.nextToken();// 得到第一个字段值
        String second = itr.nextToken();// 得到第二个字段值

        // 设置组合key和value ==> <(key,value),value>
        // 设置MyKeyPair类型的输出key
        MyKeyPair outKey = new MyKeyPair();
        outKey.setFirst(first);
        outKey.setSecond(Integer.valueOf(second));
        // 设置IntWritable类型的输出value
        IntWritable outValue = new IntWritable();
        outValue.set(Integer.valueOf(second));
        // 输出<key,value>对
        context.write(outKey, outValue);
    }
}

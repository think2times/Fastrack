package mapreduce.demo.secondsort;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import java.io.IOException;

/**
 * 定义Reducer类
 */
public class MyReducer extends
        Reducer<MyKeyPair, IntWritable, Text, IntWritable> {
    /**
     * 重写reduce()方法
     */
    public void reduce(MyKeyPair key, Iterable<IntWritable> values,
            Context context) throws IOException, InterruptedException {
        // 定义Text类型的输出key
        Text outKey = new Text();
        // 迭代输出<key,value>对
        for (IntWritable value : values) {
            outKey.set(key.getFirst());
            context.write(outKey, value);
        }
    }
}

package hbase.demo.mr;

import java.io.IOException;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableReducer;
import org.apache.hadoop.io.NullWritable;

/**
 * 将数据写入到HBase另一张表student_new中
 */
public class WriteStudentReducer extends
        TableReducer<ImmutableBytesWritable, Put, NullWritable> {
    /**
     * 接收map()函数的输出 参数key和values的类型需与map()函数的输出一致
     */
    protected void reduce(ImmutableBytesWritable key, Iterable<Put> values,
            Context context) throws IOException, InterruptedException {
        for (Put put : values) {
            // 将数据写入HBase表中，输出的key可以为空，因为行键在put对象中已经包含
            context.write(NullWritable.get(), put);
        }
    }
}

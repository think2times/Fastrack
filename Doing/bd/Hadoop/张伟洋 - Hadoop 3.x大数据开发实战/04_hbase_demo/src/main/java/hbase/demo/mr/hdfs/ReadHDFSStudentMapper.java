package hbase.demo.mr.hdfs;

import java.io.IOException;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

/**
 * 读取HDFS中的文件student.txt数据
 */
public class ReadHDFSStudentMapper extends
        Mapper<LongWritable, Text, ImmutableBytesWritable, Put> {
    /**
     * 接收HDFS中的数据 参数key为一行数据的下标位置，value为一行数据
     */
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {
        // 将读取的一行数据转为字符串
        String lineValue = value.toString();
        // 将一行数据根据“\t”分割成String数组
        String[] values = lineValue.split("\t");
        // 取出每一个值
        String rowKey = values[0];// 学号
        String name = values[1];// 姓名
        String age = values[2];// 年龄
        // 将rowKey转为ImmutableBytesWritable类型，便于Reduce阶段接收
        ImmutableBytesWritable rowKeyWritable = new ImmutableBytesWritable(
                Bytes.toBytes(rowKey));
        // 创建Put对象，用于存储一整行数据
        Put put = new Put(Bytes.toBytes(rowKey));
        // 向Put对象中添加数据，参数分别为:列族、列、值
        put.addColumn(Bytes.toBytes("info"), Bytes.toBytes("name"),
                Bytes.toBytes(name));
        put.addColumn(Bytes.toBytes("info"), Bytes.toBytes("age"),
                Bytes.toBytes(age));
        // 写数据到Reduce阶段，键为HBase表的rowkey（学号），值为Put对象
        context.write(rowKeyWritable, put);
    }
}

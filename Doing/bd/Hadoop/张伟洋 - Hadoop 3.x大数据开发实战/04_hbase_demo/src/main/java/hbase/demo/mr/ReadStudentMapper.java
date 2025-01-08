package hbase.demo.mr;

import java.io.IOException;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapper;
import org.apache.hadoop.hbase.util.Bytes;

/**
 * 从HBase中读取表student的指定列的数据
 */
public class ReadStudentMapper extends TableMapper<ImmutableBytesWritable, Put> {
    /**
     * 参数key为表中的行键，value为行键对应的一行数据的集合
     */
    protected void map(ImmutableBytesWritable key, Result value, Context context)
            throws IOException, InterruptedException {
        // 新建put对象，传入行键
        Put put = new Put(key.get());
        // 遍历一行数据的每一个单元格
        for (Cell cell : value.rawCells()) {
            // 如果当前单元格所属列族为info
            if ("info".equals(Bytes.toString(CellUtil.cloneFamily(cell)))) {
                // 如果当前单元格的列限定符为name
                if ("name".equals(Bytes.toString(CellUtil.cloneQualifier(cell)))) {
                    // 将该单元格加入到put对象中
                    put.add(cell);
                    // 如果当前单元格的列限定符为age
                } else if ("age".equals(Bytes.toString(CellUtil
                        .cloneQualifier(cell)))) {
                    // 将该单元格加入到put对象中
                    put.add(cell);
                }
            }
        }
        // 将Put对象写入到context中作为map的输出
        context.write(key, put);
    }
}

package mapreduce.demo.secondsort;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.mapreduce.Partitioner;

/**
 * 自定义分区类
 */
public class MyPartitioner extends Partitioner<MyKeyPair, IntWritable> {
    /**
     * 实现抽象方法getPartition()，自定义分区字段
     * 
     * @param myKeyPair
     *            :<key,value>对中key的类型
     * @param value
     *            :<key,value>对中value的类型
     * @param numPartitions
     *            :分区的数量
     * @return 分区编号
     */
    public int getPartition(MyKeyPair myKeyPair, IntWritable value,
            int numPartitions) {
        // 根据第一个字段作为分区字段
        return (myKeyPair.getFirst().hashCode() & Integer.MAX_VALUE)
                % numPartitions;
    }
}

package hbase.demo.mr;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.mapreduce.Job;

/**
 * MapReduce任务构建与执行类
 */
public class StudentMRRunner {
    /**
     * main方法，任务执行的入口
     */
    public static void main(String[] args) throws Exception {
        // 创建Configuration实例
        Configuration conf = HBaseConfiguration.create();
        // 创建Job任务,指定任务名称
        Job job = Job.getInstance(conf, "hbase_mr_job");
        // 设置任务运行主类
        job.setJarByClass(StudentMRRunner.class);
        // 创建Scan数据扫描对象
        Scan scan = new Scan();
        // 是否缓存块数据，默认true。设置为false节省了交换缓存的操作消耗，可以提升MR任务的效率
        // MR任务必须设置为false
        scan.setCacheBlocks(false);
        // 每次RPC请求从HBase表中取得的数据行数
        scan.setCaching(500);
        // 初始化Mapper任务
        // 注意导入的是mapreduce包下的，不是mapred包下的，后者是老版本
        TableMapReduceUtil.initTableMapperJob("student", // 数据源表名
                scan, // scan扫描控制器
                ReadStudentMapper.class, // 指定Mapper类
                ImmutableBytesWritable.class, // Mapper输出的key类型
                Put.class, // Mapper输出的value类型
                job// 指定任务job
                );
        // 初始化Reducer任务
        TableMapReduceUtil.initTableReducerJob("student_new",// 数据目的地表名
                WriteStudentReducer.class, job);// 指定Reducer类与任务job
        // 设置Reduce数量，最少1个
        job.setNumReduceTasks(1);
        // 执行任务
        boolean isSuccess = job.waitForCompletion(true);
        if (!isSuccess) {
            throw new IOException("任务运行错误！！");
        }
        System.exit(isSuccess ? 0 : 1);
    }
}

package mapreduce.demo.test;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.mapreduce.Job;

//程序入口类
public class MyMRApplication {

    public static void main(String[] args) throws Exception {
        // 构建Configuration实例
        Configuration conf = new Configuration();
        // 其它配置信息代码...
        // 获得Job实例
        Job job = Job.getInstance(conf, "My job name");
        // 其它job配置代码...
        // 设置MapperReduce处理类
        job.setMapperClass(MyMapper.class);
        // job.setCombinerClass(MyReducer.class);

        // 设置输入和输出目录...
        // 提交任务

    }
}

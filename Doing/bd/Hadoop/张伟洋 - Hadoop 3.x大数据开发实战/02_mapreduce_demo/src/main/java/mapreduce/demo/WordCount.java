package mapreduce.demo;

import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

/** 单词计数类 **/
public class WordCount {
    // 程序入口main函数
    public static void main(String[] args) throws Exception {
        // 初始化Configuration类
        Configuration conf = new Configuration();
        // 通过实例化对象GenericOptionsParser可以获得程序执行所传入的参数
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length < 2) {
            System.err.println("Usage: wordcount <in> [<in>...] <out>");
            System.exit(2);
        }
        // 构建任务对象
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        // 设置输出结果的数据类型
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        for (int i = 0; i < otherArgs.length - 1; i++) {
            // 设置需要统计的文件的输入路径
            FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
        }
        // 设置统计结果的输出路径
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[(otherArgs.length - 1)]));
        // 提交任务给Hadoop集群
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

    public static class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Reducer<Text, IntWritable, Text, IntWritable>.Context context) throws IOException,
                InterruptedException {
            // 统计单词总数
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            this.result.set(sum);
            // 输出统计结果
            context.write(key, this.result);
        }
    }

    public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable> {
        private static final IntWritable one = new IntWritable(1);
        private Text word = new Text();

        public void map(Object key, Text value, Mapper<Object, Text, Text, IntWritable>.Context context) throws IOException, InterruptedException {
            // 默认根据空格、制表符\t、换行符\n、回车符\r分割字符串
            StringTokenizer itr = new StringTokenizer(value.toString());
            // 循环输出每个单词与数量
            while (itr.hasMoreTokens()) {
                this.word.set(itr.nextToken());
                // 输出单词与数量
                context.write(this.word, one);
            }
        }
    }
}

package mapreduce.demo;

import java.io.IOException;
import java.util.Iterator;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

/**
 * 求平均分例子
 */
public class Score {

    public static class Map extends
            Mapper<LongWritable, Text, Text, IntWritable> {
        // 实现map函数
        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {
            // 将输入的一行数据转化成String
            // String line = value.toString();
            // 处理中文乱码，Hadoop默认是UTF-8编码，如果中文GBK编码的字符，则会出现乱码，需要以下面的方式进行转码
            String line = new String(value.getBytes(), 0, value.getLength(),
                    "UTF-8");
            // 将输入的一行数据默认按空格、制表符\t、换行符\n、回车符\r进行分割，也可以加入一个参数指定分隔符
            StringTokenizer itr = new StringTokenizer(line);
            // 获取分割后的字符串
            String strName = itr.nextToken();// 学生姓名部分
            String strScore = itr.nextToken();// 成绩部分
            Text name = new Text(strName);
            int scoreInt = Integer.parseInt(strScore);
            // 输出姓名和成绩
            context.write(name, new IntWritable(scoreInt));
        }
    }

    public static class Reduce extends
            Reducer<Text, IntWritable, Text, IntWritable> {
        // 实现reduce函数
        public void reduce(Text key, Iterable<IntWritable> values,
                Context context) throws IOException, InterruptedException {
            int sum = 0;
            int count = 0;
            Iterator<IntWritable> iterator = values.iterator();
            while (iterator.hasNext()) {
                sum += iterator.next().get();// 计算总分
                count++;// 统计总的科目数
            }

            int average = (int) sum / count;// 计算平均成绩
            // 输出姓名和平均成绩
            context.write(key, new IntWritable(average));
        }

    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        // 这句话很关键
        conf.set("fs.default.name", "hdfs://192.168.170.133:9000");
        // conf.setLong("mapred.min.split.size",10);
        Job job = Job.getInstance(conf, "Score Average");
        job.setJarByClass(Score.class);

        // 设置Map、Reduce处理类
        job.setMapperClass(Map.class);
        job.setReducerClass(Reduce.class);

        // 设置输出类型
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        // 将输入的数据集分割成小数据块splites，提供一个RecordReder的实现
        job.setInputFormatClass(TextInputFormat.class);
        // 提供一个RecordWriter的实现，负责数据输出
        job.setOutputFormatClass(TextOutputFormat.class);

        // 设置输入和输出目录
        FileInputFormat.addInputPath(job, new Path("/input/"));
        FileOutputFormat.setOutputPath(job, new Path("/output"));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
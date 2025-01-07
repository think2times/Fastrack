package mapreduce.demo;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mrunit.mapreduce.MapDriver;
import org.apache.hadoop.mrunit.mapreduce.MapReduceDriver;
import org.apache.hadoop.mrunit.mapreduce.ReduceDriver;
import org.apache.hadoop.mrunit.types.Pair;
import org.junit.Before;
import org.junit.Test;

/**
 * MapReduce测试类
 */
public class MRTest {
    // Map测试驱动类，泛型类型与Map类一致
    MapDriver<Object, Text, Text, IntWritable> mapDriver;
    // Reduce测试驱动类，泛型类型与Reduce类一致
    ReduceDriver<Text, IntWritable, Text, IntWritable> redeceDriver;
    // MapReduce测试驱动类，泛型类型前四个与Map类的类型一致，后两个与Reduce类的输出一致
    MapReduceDriver<Object, Text, Text, IntWritable, Text, IntWritable> mapReduceDriver;

    /**
     * 测试方法运行前的变量赋值
     */
    @Before
    public void setUp() {
        WordCount.TokenizerMapper mapper = new WordCount.TokenizerMapper();
        WordCount.IntSumReducer reducer = new WordCount.IntSumReducer();
        // 指定需要测试的Map类
        mapDriver = MapDriver.newMapDriver(mapper);
        // 指定需要测试的Reduce类
        redeceDriver = ReduceDriver.newReduceDriver(reducer);
        // 指定需要测试的Map与Reduce类
        mapReduceDriver = MapReduceDriver.newMapReduceDriver(mapper, reducer);
    }

    /**
     * 测试Map类 若结果与期望输出数据相匹配则测试成功
     */
    @Test
    public void testMapper() throws IOException {
        // 设置Map的输入数据
        mapDriver.withInput(new IntWritable(1), new Text(
                "hello world hello hadoop"));
        // 设置Map的输出数据
        mapDriver.withOutput(new Text("hello"), new IntWritable(1))
                .withOutput(new Text("world"), new IntWritable(1))
                .withOutput(new Text("hello"), new IntWritable(1))
                .withOutput(new Text("hadoop"), new IntWritable(1));
        mapDriver.runTest();
    }

    /**
     * 测试Reduce类 若结果与期望输出数据相匹配则测试成功
     */
    @Test
    public void testReducer() throws Exception {
        // 声明输入数据
        List<IntWritable> values = new ArrayList<IntWritable>();
        values.add(new IntWritable(1));
        values.add(new IntWritable(1));
        // 设置输入数据与输出数据
        redeceDriver.withInput(new Text("hello"), values)
                .withOutput(new Text("hello"), new IntWritable(2)).runTest();
    }

    /**
     * 测试MapReduce 传入Map的输入数据与Reduce的期望输出数据，若结果与期望输出数据相匹配，则测试成功
     */
    @Test
    public void testMapReduce() throws IOException {
        // 声明Map输入数据
        Text value = new Text("hello world hello hadoop");
        // 声明Reduce输出数据，注意集合元素的顺序
        List<Pair<Text, IntWritable>> outputs = new ArrayList<Pair<Text, IntWritable>>();
        outputs.add(new Pair(new Text("hadoop"), new IntWritable(1)));
        outputs.add(new Pair(new Text("hello"), new IntWritable(2)));
        outputs.add(new Pair(new Text("world"), new IntWritable(1)));
        // 设置输入与输出数据并执行测试
        mapReduceDriver.withInput(new LongWritable(0), value)
                .withAllOutput(outputs).runTest();
    }

    public static void main(String[] args) {
        System.out.println("u1000".hashCode() % 3);
    }

}
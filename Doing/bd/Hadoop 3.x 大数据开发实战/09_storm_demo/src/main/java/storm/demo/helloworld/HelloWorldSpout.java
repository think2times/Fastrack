package storm.demo.helloworld;

import java.util.Map;
import java.util.Random;

import org.apache.storm.spout.SpoutOutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichSpout;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;
import org.apache.storm.utils.Utils;

public class HelloWorldSpout extends BaseRichSpout {

    /**
     * 功能：随机生成字符串
     * 实现：先产生一个1-10随机整数，再不断产生一个1-10随机整数，若两者
     * 相等，则发射hello world，否则发送其他字符串
     */
    private static final long serialVersionUID = -5698117627723074157L;
    private static final int MAX_RANDOM = 10;
    private int referenceRandom;
    private SpoutOutputCollector collector;

    //构造函数
    public HelloWorldSpout() {
        //产生第一个随机数
        final Random rand = new Random();
        referenceRandom = rand.nextInt(MAX_RANDOM);
    }

    //在spout加载时，打开一些资源（只在spout加载的时候执行一次）
    public void open(Map conf, TopologyContext context, SpoutOutputCollector collector) {
        this.collector = collector;

    }

    //核心方法，storm会不断调用该方法，也就是方法执行完后会马上重置并再次执行
    public void nextTuple() {

        Utils.sleep(1000);//停滞一秒
        final Random rand = new Random();
        int instanceRandom = rand.nextInt(MAX_RANDOM);
        if (referenceRandom == instanceRandom) {
            collector.emit(new Values("Hello World"));//有顺序的
        } else {
            collector.emit(new Values("Other Random Word"));
        }

    }

    //声明Tuple的字段名，有顺序的
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("sentence"));

    }

}

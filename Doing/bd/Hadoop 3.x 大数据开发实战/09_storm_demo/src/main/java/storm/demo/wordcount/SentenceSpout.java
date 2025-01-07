package storm.demo.wordcount;

import java.util.Map;
import java.util.Random;

import org.apache.storm.spout.SpoutOutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichSpout;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;
import org.apache.storm.utils.Utils;

/**
 * 消息源Spout类：随机选取一句英文语句作为源，发射出去
 */
public class SentenceSpout extends BaseRichSpout {

    private static final long serialVersionUID = -7931319401402491006L;
    private SpoutOutputCollector spoutoutputcollector;
    Random random;
    private String[] sentences = { "Apache Storm is a free and open source distributed realtime computation system",
            "Storm makes it easy to reliably process unbounded streams of data doing for ",
            "realtime processing what Hadoop did for batch processing Storm is simple ",
            "can be used with any programming language and is a lot of fun to use ", "Storm has many use cases realtime analytics ",
            "a benchmark clocked it at over a million tuples processed per second per node ",
            "Storm integrates with the queueing and database technologies you already use ", };

    /**
     * 进行Spout的一些初始化工作
     */
    public void open(Map conf, TopologyContext topologycontext, SpoutOutputCollector spoutoutputcollector) {
        this.spoutoutputcollector = spoutoutputcollector;
        random = new Random();
    }

    /**
     * 每两秒钟发射一次数据
     */
    public void nextTuple() {
        Utils.sleep(2000);
        //从sentences数组中随机选取一句话作为发送的消息
        String sentence = sentences[random.nextInt(sentences.length)];
        //发送Tuple
        this.spoutoutputcollector.emit(new Values(sentence));
    }

    /**
     * 定义字段名称，对应emit(new Values(sentence))中的字段
     */
    public void declareOutputFields(OutputFieldsDeclarer outputfieldsdeclarer) {
        outputfieldsdeclarer.declare(new Fields("sentence"));
    }

}
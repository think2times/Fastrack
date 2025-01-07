package storm.kafka.demo.topology;

import org.apache.storm.topology.BasicOutputCollector;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseBasicBolt;
import org.apache.storm.tuple.Tuple;

/**
 * Bolt类，用于将接收到的消息打印到控制台
 */
public class PrintBolt extends BaseBasicBolt {

    private static final long serialVersionUID = 1L;

    /**
     * 接收Tuple数据进行处理
     * @param tuple
     *         接收到的Tuple数据
     * @param basicOutputCollector
     *         用于将Tuple向外进行发射
     */
    public void execute(Tuple tuple, BasicOutputCollector basicOutputCollector) {
        // 打印接收到的消息
        // 收到的Tuple是一个数组，例如：[topictest, 1, 4, null, hello kafka storm]
        // 打印Tuple中位置为4的字段值（也就是消息的内容），位置从0开始
        System.out.println(tuple.getValue(4));
        // 打印Tuple中的所有字段值
        System.out.println(tuple.getValues());
    }

    /**
     * 向外发射的Tuple的字段声明
     */
    public void declareOutputFields(OutputFieldsDeclarer outputFieldsDeclarer) {
    }
}

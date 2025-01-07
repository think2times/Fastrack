package storm.kafka.demo.spouts;

import java.time.Duration;
import java.util.Arrays;
import java.util.Map;
import java.util.Properties;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.storm.spout.SpoutOutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichSpout;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Values;

/**
 * Spout类，从Kafka中读取消息并发送出去
 */
public class KafkaSpout extends BaseRichSpout {

    private static final long serialVersionUID = 7582771881226024741L;
    // 定义Kafka消费者对象
    private KafkaConsumer<String, String> consumer;
    // 该对象用于发射Tuple
    SpoutOutputCollector collector;

    /**
     * 进行Spout的一些初始化工作并提供Spout的执行环境，当该Spout在集群的Worker中被初始化时会调用该方法
     * 
     * @param conf
     *            Spout的配置信息
     * @param context
     *            此对象可用于获取此Task在Topology中的位置的信息，包括此Task的Task id和component
     *            id、输入和输出信息等。
     * @param collector
     *            用于发射Tuple。Tuple可以在任何时候任何方法中发出，包括open()和close()方法。
     *            collector是线程安全的， 可以作为该Spout对象的实例变量保存。
     */
    public void open(Map conf, TopologyContext context, SpoutOutputCollector collector) {
        this.collector = collector;

        // Kafka属性信息
        Properties props = new Properties();
        props.put("bootstrap.servers", "centos01:9092,centos02:9092,centos03:9092");
        props.put("group.id", "test");// 消费者组id（组名称）
        // 反序列化key的程序类
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        // 反序列化value的程序类
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        // 实例化消费者类
        consumer = new KafkaConsumer<String, String>(props);
        // 设置消费主题
        consumer.subscribe(Arrays.asList("myTopic"));

    }

    /**
     * 从Kafka中拉取数据并发射出去 当Storm需要Spout发射Tuple时会调用该方法（循环调用）
     */
    public void nextTuple() {
        // 拉取消息记录，超时时间为10秒
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(10));
        for (ConsumerRecord<String, String> record : records) {
            String key = record.key();// 消息key值
            String value = record.value();// 消息value值
            // 发射Tuple
            collector.emit(new Values(key, value));
        }
    }

    /**
     * 定义字段名称，对应emit(new Values(sentence))中的字段
     */
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        declarer.declare(new Fields("key", "value"));
    }

}

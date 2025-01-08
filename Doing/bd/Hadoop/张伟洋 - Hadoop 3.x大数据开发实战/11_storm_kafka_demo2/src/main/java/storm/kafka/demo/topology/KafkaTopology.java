package storm.kafka.demo.topology;

import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.StormSubmitter;
import org.apache.storm.kafka.spout.KafkaSpout;
import org.apache.storm.kafka.spout.KafkaSpoutConfig;
import org.apache.storm.topology.TopologyBuilder;

/**
 * Topology类，用于在Storm中构建一个Topology
 */
public class KafkaTopology {
    public static void main(String[] args) throws Exception {

        // 1. 创建KafkaSpout对象
        KafkaSpoutConfig.Builder<String, String> kafkaBuilder = 
                KafkaSpoutConfig.builder("centos01:9092,centos02:9092,centos03:9092", "topictest");
        // 设置kafka消费者组ID
        kafkaBuilder.setProp("group.id", "testgroup");
        // 创建kafkaSpoutConfig
        KafkaSpoutConfig<String, String> kafkaSpoutConfig = kafkaBuilder.build();
        // 通过kafkaSpoutConfig获得KafkaSpout对象
        KafkaSpout<String, String> kafkaSpout = new KafkaSpout<String, String>(kafkaSpoutConfig);

        // 2. 创建一个Topology
        TopologyBuilder builder = new TopologyBuilder();
        // 设置Spout，并行度为2（线程数）
        builder.setSpout("kafka-Spout", kafkaSpout, 2);
        // 设置Bolt，并行度为2（线程数）,流分组方式为localOrShuffleGrouping（本地或随机）
        builder.setBolt("print-Bolt", new PrintBolt(), 2).localOrShuffleGrouping("kafka-Spout");

        Config config = new Config();
        if (args.length > 0) {
            // 集群提交模式
            config.setDebug(false);
            StormSubmitter.submitTopology("kafka-Topology", config, builder.createTopology());
        } else {
            // 本地测试模式
            config.setDebug(false);
            // 设置Worker进程的数量为2
            config.setNumWorkers(2);
            LocalCluster cluster = new LocalCluster();
            cluster.submitTopology("kafka-Topology", config, builder.createTopology());
        }
    }
}

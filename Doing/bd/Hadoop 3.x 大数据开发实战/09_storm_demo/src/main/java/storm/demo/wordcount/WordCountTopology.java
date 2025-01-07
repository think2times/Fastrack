package storm.demo.wordcount;
import org.apache.storm.Config;  
import org.apache.storm.LocalCluster;  
import org.apache.storm.StormSubmitter;
import org.apache.storm.generated.AlreadyAliveException;
import org.apache.storm.generated.AuthorizationException;
import org.apache.storm.generated.InvalidTopologyException;
import org.apache.storm.topology.TopologyBuilder;  
import org.apache.storm.tuple.Fields;  
  
public class WordCountTopology {  
  
    public static void main(String[] args) throws Exception {  
        SentenceSpout sentenceSpout = new SentenceSpout();  
        SplitSentenceBolt splitSentenceBolt = new SplitSentenceBolt();  
        WordCountBolt wordCountBolt = new WordCountBolt();  
        ReportBolt reportBolt = new ReportBolt();  
  
        //创建一个拓扑
        TopologyBuilder topologyBuilder = new TopologyBuilder();  
        //设置Spout，名称为"sentence-spout"，并行度为2(也就是线程数)，任务数为4(也就是实例数)。默认是1个线程，1个任务。  如果不指定Task数量，则一个线程执行一个Task，Task数量与线程数量一样。
        topologyBuilder.setSpout("sentence-spout", sentenceSpout,2).setNumTasks(4);  
        //设置bolt，名称为"split-bolt",数据来源是名称为"sentence-spout"的spout，
        //ShuffleGrouping：随机选择一个Task来发送,对Task的分配比较均匀。
        topologyBuilder.setBolt("split-bolt", splitSentenceBolt,2).setNumTasks(4).shuffleGrouping("sentence-spout");  
        //FiledGrouping：根据Tuple中Fields来做一致性hash，相同hash值的Tuple被发送到相同的Task。
        topologyBuilder.setBolt("count-bolt", wordCountBolt,2).setNumTasks(4).fieldsGrouping("split-bolt", new Fields("word"));  
        //GlobalGrouping：所有的Tuple会被发送到某个Bolt中的id最小的那个Task,此时不管有多少个Task，只发往一个Task
        topologyBuilder.setBolt("report-bolt", reportBolt,2).setNumTasks(4).globalGrouping("count-bolt");  
  
        Config config = new Config();  
        //本地模式 ，第一个参数为定义拓扑名称
        LocalCluster cluster = new LocalCluster();  
        cluster.submitTopology("word-count-topology", config, topologyBuilder.createTopology());  
       /* Utils.sleep(5000);  
        cluster.killTopology(TOPOLOGY_NAME);  
        cluster.shutdown();  */
        
        //集群模式，需要打包jar上传到集群，然后使用命令 :storm jar storm_demo-0.0.1-SNAPSHOT.jar com.zwy.storm.demo.wordcount.WordCountTopology
/*        config.setNumWorkers(2); //设置Worker进程数量 
//        config.setNumAckers(0);//设置acker并发数，0代表取消acker任务。Acker任务默认是每个worker进程启动一个executor线程来执行,该实例启动了2个worker，则默认会启动2个executor线程,2个acker任务
        StormSubmitter.submitTopology("word-count-topology",config,topologyBuilder.createTopology());*/
	
        
        
    }  
}  
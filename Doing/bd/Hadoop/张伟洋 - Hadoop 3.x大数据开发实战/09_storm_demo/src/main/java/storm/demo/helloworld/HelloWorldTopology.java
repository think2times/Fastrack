package storm.demo.helloworld;

import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.StormSubmitter;
import org.apache.storm.generated.AlreadyAliveException;
import org.apache.storm.generated.AuthorizationException;
import org.apache.storm.generated.InvalidTopologyException;
import org.apache.storm.topology.TopologyBuilder;
import org.apache.storm.utils.Utils;

public class HelloWorldTopology {

    //可以向main传递一个参数作为集群模式下的Topology的名字，若没有传入参数则使用本地模式
    public static void main(String[] args) {

        TopologyBuilder builder = new TopologyBuilder();

        builder.setSpout("hlSpout", new HelloWorldSpout());
        builder.setBolt("hlBolt", new HelloWorldBolt()).shuffleGrouping("hlSpout");

        Config conf = new Config();

        if (args != null && args.length > 0) {
            //集群模式提交
            conf.setNumWorkers(3);

            try {
                StormSubmitter.submitTopology(args[0], conf, builder.createTopology());
            } catch (Exception e) {
                e.printStackTrace();
            }

        } else {
            try {
                //本地模式提交
                LocalCluster cluster = new LocalCluster();
                cluster.submitTopology("test", conf, builder.createTopology());
                Utils.sleep(1000 * 60);
                cluster.killTopology("test");
                cluster.shutdown();
            } catch (Exception e) {
                e.printStackTrace();
            }

        }
    }

}

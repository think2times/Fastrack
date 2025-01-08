package storm.demo.helloworld;

import java.util.Map;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Tuple;

public class HelloWorldBolt extends BaseRichBolt {

    /**
     * 功能：就收到spout发送的数据，打印并统计hello world的数量
     * 实现：打印，创建计数变量用于统计hello world
     */
    private static final long serialVersionUID = -5061906223048521415L;
    private int myCount = 0;//计数变量，不能在execute函数中初始化
    private TopologyContext context;//上下文变量
    private OutputCollector collector;

    //相当于spout中的open
    public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
        this.context = context;
        this.collector = collector;

    }

    //相当于spout中的nextTuple
    public void execute(Tuple input) {

        //拿到数据，用字段名取出
        String text = input.getStringByField("sentence");
        System.out.println("One tuple gets in: " + context.getThisTaskId() + text);
        if ("Hello World".equals(text)) {
            myCount++;
            System.out.println("Found a Hello World! My count is now:" + myCount);

        }
        collector.ack(input);//处理完成要通知Storm
        //		collector.fail(input);//处理失败要通知Storm

    }

    public void declareOutputFields(OutputFieldsDeclarer declarer) {
    }

}

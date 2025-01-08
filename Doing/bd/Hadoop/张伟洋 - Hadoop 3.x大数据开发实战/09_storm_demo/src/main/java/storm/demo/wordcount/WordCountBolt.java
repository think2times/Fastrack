package storm.demo.wordcount;
import java.util.HashMap;  
import java.util.Map;  

import org.apache.storm.task.OutputCollector;  
import org.apache.storm.task.TopologyContext;  
import org.apache.storm.topology.OutputFieldsDeclarer;  
import org.apache.storm.topology.base.BaseRichBolt;  
import org.apache.storm.tuple.Fields;  
import org.apache.storm.tuple.Tuple;  
import org.apache.storm.tuple.Values;  
  
/**
 * 单词统计，并且实时获取词频前N的发射出去
 */
public class WordCountBolt extends BaseRichBolt {  
    
	private static final long serialVersionUID = 2374950653902413273L;
	private OutputCollector outputcollector;  
	//定义存放单词与词频的Map
    private HashMap<String, Integer> counts = null;  
  
    /**
     * bolt初始化方法，与spout的open()方法类似
     */
    public void prepare(Map map, TopologyContext topologycontext, OutputCollector outputcollector) {  
        this.outputcollector = outputcollector;  
        this.counts = new HashMap<String, Integer>();  
    }  
  
    /**
	 * 接收Tuple数据进行单词计数处理
	 */
    public void execute(Tuple tuple) {  
    	//获取发送过来的单词
        String word = tuple.getStringByField("word");  
        //添加这行代码的作用是看看值相等的word是不是同一个实例执行的，事实证明确实如此  
        //System.out.println(this + "====" + word);  
        //单词数量加1
        Integer count = counts.get(word);
        if (count == null)
          count = 0;
        count++;
        counts.put(word, count);
        //发送单词和计数给下一个bolt，分别对应字段"word"和"count"
        this.outputcollector.emit(new Values(word, count));  
    }
    /**
     * 设置字段名称，对应emit(new Values(word, count))中的两个字段
     */
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("word","count"));  		
	}
}
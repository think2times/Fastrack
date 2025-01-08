package storm.demo.wordcount;
import java.util.Map;  
  
import org.apache.storm.task.OutputCollector;  
import org.apache.storm.task.TopologyContext;  
import org.apache.storm.topology.OutputFieldsDeclarer;  
import org.apache.storm.topology.base.BaseRichBolt;  
import org.apache.storm.tuple.Fields;  
import org.apache.storm.tuple.Tuple;  
import org.apache.storm.tuple.Values;  
  
public class SplitSentenceBolt extends BaseRichBolt {  
	private static final long serialVersionUID = 1L;
	private OutputCollector outputcollector;  
  
	/**
	 * bolt初始化方法，与spout的open()方法类似
	 */
	public void prepare(Map map, TopologyContext topologycontext, OutputCollector outputcollector) {  
		this.outputcollector = outputcollector;  
	}  
	/**
	 * 接收Tuple数据进行处理
	 */
    public void execute(Tuple tuple) {  
    	//获取发送过来的数据（此处得到发送过来的一句话）
        String sentence = tuple.getStringByField("sentence");  
        //将数据以空格分割为单词数组
        String[] words = sentence.split(" ");  
        //逐个将单词发射出去
        for (String word : words) {  
            this.outputcollector.emit(new Values(word));  
        }  
    }  
  
    /**
     * 字段声明
     */
    public void declareOutputFields(OutputFieldsDeclarer outputfieldsdeclarer) {  
        outputfieldsdeclarer.declare(new Fields("word"));  
    }  
  
} 
package storm.demo.wordcount;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;  
import java.util.List;
import java.util.Map;  
import java.util.Map.Entry;

import org.apache.storm.task.OutputCollector;  
import org.apache.storm.task.TopologyContext;  
import org.apache.storm.topology.OutputFieldsDeclarer;  
import org.apache.storm.topology.base.BaseRichBolt;  
import org.apache.storm.tuple.Tuple;  
  
public class ReportBolt extends BaseRichBolt {  
	
	private static final long serialVersionUID = -1512537746316594950L;
	private HashMap<String, Integer> counts = null;  
  
    public void prepare(Map map, TopologyContext topologycontext, OutputCollector outputcollector) {  
        this.counts = new HashMap<String, Integer>();  
    }  
  
    public void execute(Tuple tuple) {  
        String word = tuple.getStringByField("word");  
        int count = tuple.getIntegerByField("count");  
        counts.put(word, count);  
      //对counts中的单词进行排序
        List<Entry<String,Integer>> list = new ArrayList<Entry<String,Integer>>(counts.entrySet());
		Collections.sort(list, new Comparator<Map.Entry<String, Integer>>() {
			  public int compare(Map.Entry<String, Integer> o1,
			      Map.Entry<String, Integer> o2) {
			    return (o2.getValue() - o1.getValue());
			  }
			});
        
        //取list中前10个单词
		int n=list.size()<=10?list.size():10;
		String resultStr="";
		for(int i=0;i<n;i++){
			Entry<String,Integer> entry=list.get(i);
			String sortWord=entry.getKey();
			Integer sortCount=entry.getValue();
			resultStr+="\n"+sortWord+"----"+sortCount;
		}
		System.out.println("\n------------计数结果----------------"); 
		//添加这行代码的作用是看看是不是同一个实例执行的  
//		System.out.println(this + "====" + word); 
		System.out.println(resultStr);
    }  
  
    public void declareOutputFields(OutputFieldsDeclarer outputfieldsdeclarer) {  
  
    }  
  
    /**
     * 在bolt被关闭的时候调用， 它应该清理所有被打开的资源。但是集群不保证这个方法一定会被执行。比如执行task的机器down掉了，那么根本就没有办法来调用那个方法。
     */
    public void cleanup() {  
        System.out.println("---------- FINAL COUNTS -----------");  
        for (String key : counts.keySet()) {  
            System.out.println(key + " " + counts.get(key));  
        }  
        System.out.println("----------------------------");  
    }  
}  
package hbase.demo.filter;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.filter.*;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.hbase.client.*;

public class HBaseFilterDemo {
	static Configuration conf=null;
	static{
		//创建HBase配置对象
		conf=HBaseConfiguration.create();
		//加上这一句，就不需要将代码发布到服务器中执行了，直接eclipse中运行就可以。不加这一句，需要将代码导出jar，上传到HBase服务器执行。
		conf.set("hbase.zookeeper.quorum", "centos01:2181,centos02:2181,centos03:2181");
	}
	
	public static void main(String[] args) throws Exception {
		filterTest();
		
	}
	
	/**
	 * 创建表t1 ,列族f1
	 * @throws Exception
	 */
	public static void filterTest() throws Exception {
		Connection conn=ConnectionFactory.createConnection(conf);
		//得到user_info表的连接
		Table table =conn.getTable(TableName.valueOf("t1"));
		Scan scan = new Scan();
//		RegexStringComparator comp = new RegexStringComparator("you."); // 以 you 开头的字符串
//		SingleColumnValueFilter filter = new SingleColumnValueFilter(Bytes.toBytes("family"), Bytes.toBytes("qualifier"), CompareOperator.EQUAL, comp);
		//1. 行键过滤器：筛选出行键为row2的一行数据
//		Filter filter = new RowFilter(CompareOperator.EQUAL, new BinaryComparator(Bytes.toBytes("row2"))); 
		//2. 列族过滤器：筛选出列族为f1的所有数据
//		Filter filter = new FamilyFilter(CompareOperator.EQUAL, new BinaryComparator(Bytes.toBytes("f1")));
		//3. 列过滤器：筛选出列为name的所有数据
//		Filter filter = new QualifierFilter(CompareOperator.EQUAL, new BinaryComparator(Bytes.toBytes("name"))); 
		//4. 值过滤器：筛选出一行中的值包含"beijing"的所有单元格数据
//		Filter filter = new ValueFilter(CompareOperator.EQUAL, new SubstringComparator("beijing"));
		//5. 单列值过滤器：用一列的值决定该行是否被过滤
		//筛选出name列不包含xiaoming的所有行数据
		Filter filter = new SingleColumnValueFilter(Bytes.toBytes("f1"), Bytes.toBytes("name"),CompareOperator.NOT_EQUAL, new SubstringComparator("xiaoming"));  
		//如果某行列name不存在，那么该行将被过滤掉，false则不进行过滤，默认为false。
		((SingleColumnValueFilter) filter).setFilterIfMissing(true);
		
		
		scan.setFilter(filter);
		ResultScanner rs = table.getScanner(scan);  
	    for (Result res : rs) {  
//	      System.out.println(res);  
	      printResult(res);
	      
	    }  
		 /*for (Result result : rs){
            for (Cell cell:result.rawCells()){
                System.out.println("Cell: "+cell+", Value: "+Bytes.toString(cell.getValueArray(),cell.getValueLength()));
            }
        }*/
		 
	    rs.close();  
	}
	
	public static void printResult(Result res){
		if(!res.toString().equals("keyvalues=NONE")){
			for(Cell cell:res.listCells()){
				if(null!=cell){
				    //取得rowkey
				    String rowkey = new String(CellUtil.cloneRow(cell));
				    //取得当前单元格所属的列族名称
                    String family = new String(CellUtil.cloneFamily(cell));
                    //取得当前单元格所属的列名称
                    String qualifier=new String(CellUtil.cloneQualifier(cell));
                    //取得当前单元格的列值
                    String value=new String(CellUtil.cloneValue(cell));
                    //输出结果
                    System.out.println("rowkey:"+rowkey+",列： " + family+":"+qualifier + "—————值:" + value); 
				}
					
			}
		}
	}
	
}

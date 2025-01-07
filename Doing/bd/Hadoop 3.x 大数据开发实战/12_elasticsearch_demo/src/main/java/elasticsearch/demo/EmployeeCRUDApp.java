package elasticsearch.demo;

import org.apache.http.HttpHost;
import org.elasticsearch.action.delete.DeleteRequest;
import org.elasticsearch.action.delete.DeleteResponse;
import org.elasticsearch.action.get.GetRequest;
import org.elasticsearch.action.get.GetResponse;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.action.update.UpdateRequest;
import org.elasticsearch.action.update.UpdateResponse;
import org.elasticsearch.common.xcontent.XContentType;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestHighLevelClient;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * 员工信息增删改查
 */
public class EmployeeCRUDApp {

    public static void main(String[] args) throws Exception {
        RestHighLevelClient client = new RestHighLevelClient(
                RestClient.builder(
                        new HttpHost("192.168.170.133", 9200, "http")
                        // 如果是集群，可以构建多个
                        /*,new HttpHost("192.168.170.134", 9200, "http")*/
                )
        );

        // 添加员工信息
        // addEmploy(client);
        // 更新员工信息
        undateEmployee(client);
        // 删除员工信息
        // delEmployee(client);
        // 查询员工信息
        // getEmployee(client);
        // 关闭连接
        client.close();
    }

    /**
     * 添加员工信息
     */
    public static void addEmploy(RestHighLevelClient client) throws Exception {
        // 构建JSON对象
        String indexName = "company";
        IndexRequest request = new IndexRequest(indexName);
        request.source("{\"name\":\"zhangsan\",\"position\":\"software engineer\",\"country\":\"China\",\"salary\":\"10000\"}",XContentType.JSON);
        request.id("1");
        IndexResponse response = client.index(request,RequestOptions.DEFAULT);
        //输出返回结果
        System.out.println(response.getResult().toString());
    }

    /**
     * 更新员工信息
     */
    public static void undateEmployee(RestHighLevelClient client) throws Exception {
        
        // Map存储要修改的指定内容
        Map<String,Object> doc= new HashMap<String, Object>();
        doc.put("name","zhangsan");
        // 修改id为1的文档信息
        UpdateRequest request=new UpdateRequest("company","1");
        request.doc(doc);
        UpdateResponse update=client.update(request,RequestOptions.DEFAULT);
        System.out.println(update.getResult().toString());

	
    }

    /**
     * 查询员工信息
     */
    public static void getEmployee(RestHighLevelClient client) throws IOException {
        GetRequest request = new GetRequest("company", "1");
        GetResponse response = client.get(request, RequestOptions.DEFAULT);
        // 打印结果内容
        System.out.println(response.getSourceAsString());
        // 打印结果集合
        System.out.println(response.getSource().entrySet());
        // 打印结果对象
        System.out.println(response);

	
    }

    /**
     * 删除员工信息
     */
    public static void delEmployee(RestHighLevelClient client) throws IOException {
        // 执行删除，删除id为1的员工信息
        String indexName = "company";
        DeleteRequest request = new DeleteRequest(indexName);
        request.id("1");
        DeleteResponse response=client.delete(request,RequestOptions.DEFAULT);
        // 打印结果内容
        System.out.println(response.getResult().toString());

    }

}
package hdfs.demo;

import java.io.InputStream;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;

/**
 * 查询HDFS文件内容并输出
 */
public class FileSystemCat {
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        // 设置HDFS访问地址
        conf.set("fs.default.name", "hdfs://192.168.170.133:9000");
        // 取得FileSystem文件系统实例
        FileSystem fs = FileSystem.get(conf);
        // 打开文件输入流
        InputStream in = fs.open(new Path("hdfs:/input/README.txt"));
        // 输出文件内容
        IOUtils.copyBytes(in, System.out, 4096, false);
        // 关闭输入流
        IOUtils.closeStream(in);
    }
}

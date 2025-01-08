package hdfs.demo;

import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

/**
 * 创建HDFS目录mydir
 */
public class CreateDir {
    public static void main(String[] args) throws IOException {
        Configuration conf = new Configuration();
        conf.set("fs.default.name", "hdfs://192.168.170.133:9000");
        FileSystem hdfs = FileSystem.get(conf);
        // 创建目录
        boolean isok = hdfs.mkdirs(new Path("hdfs:/mydir"));
        if (isok) {
            System.out.println("创建目录成功!");
        } else {
            System.out.println("创建目录失败！");
        }
        hdfs.close();
    }
}

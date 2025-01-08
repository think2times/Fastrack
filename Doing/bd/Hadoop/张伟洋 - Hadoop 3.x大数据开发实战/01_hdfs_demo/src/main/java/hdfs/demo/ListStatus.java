package hdfs.demo;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

/**
 * 递归遍历目录和文件
 */
public class ListStatus {
	private static FileSystem hdfs;
	public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        conf.set("fs.default.name", "hdfs://192.168.170.133:9000");
        hdfs = FileSystem.get(conf);
        //遍历HDFS上的文件和目录 
        FileStatus[] fs = hdfs.listStatus(new Path("hdfs:/")); 
        if (fs.length > 0) { 
            for (FileStatus f : fs) { 
                showDir(f);
            }
        }
	}
	 private static void showDir(FileStatus fs) throws Exception {
         Path path = fs.getPath();
         //输出文件或目录的路径
         System.out.println(path);
         //如果是目录，则递归遍历该目录下的所有子目录或文件
         if (fs.isDirectory()) {
             FileStatus[] f = hdfs.listStatus(path);
             if (f.length > 0) {
                 for (FileStatus file : f) {
                     showDir(file);
                 }
             }
         }
     }
}

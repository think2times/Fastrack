package mapreduce.demo.secondsort;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import org.apache.hadoop.io.WritableComparable;

/**
 * 自定义组合key类
 */
public class MyKeyPair implements WritableComparable<MyKeyPair> {
    // 组合key属性
    private String first;// 第一个排序字段
    private int second;// 第二个排序字段

    /**
     * 实现该方法，反序列化对象input中的字段
     */
    public void readFields(DataInput input) throws IOException {
        this.first = input.readUTF();
        this.second = input.readInt();
    }

    /**
     * 实现该方法，序列化对象output中的字段
     */
    public void write(DataOutput output) throws IOException {
        output.writeUTF(first);
        output.writeInt(second);
    }

    /**
     * 实现比较器
     */
    public int compareTo(MyKeyPair o) {
        // 默认升序排列
        int res = this.first.compareTo(o.first);
        if (res != 0) {// 若第一个字段不相等，则返回
            return res;
        } else { // 若第一个字段相等，则比较第二个字段，且降序排列
            return -Integer.valueOf(this.second).compareTo(
                    Integer.valueOf(o.getSecond()));
        }
    }

    /**
     * 字段的get和set方法
     */
    public int getSecond() {
        return second;
    }

    public void setSecond(int second) {
        this.second = second;
    }

    public String getFirst() {
        return first;
    }

    public void setFirst(String first) {
        this.first = first;
    }
}
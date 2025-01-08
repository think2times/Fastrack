package mapreduce.demo.secondsort;

import org.apache.hadoop.io.WritableComparator;

/**
 * 自定义分组类
 */
public class MyGroupComparator extends WritableComparator {

    protected MyGroupComparator() {
        // 指定分组key的类型，true为创建该类型的实例，若不指定类型，将报空值错误。
        super(MyKeyPair.class, true);
    }

    // 重写compare()方法，以第一个字段进行分组
    public int compare(MyKeyPair o1, MyKeyPair o2) {
        return o1.getFirst().compareTo(o2.getFirst());
    }

}

package hive.demo;

import org.apache.hadoop.hive.ql.exec.UDF;
import org.apache.hadoop.io.Text;

/**
 * Hive自定义函数类
 */
public class MyUDF extends UDF {
    /**
     * @param text
     *            调用函数时需要传入的参数
     * @return 隐藏后的手机号码 自定义函数类需要有一个名为evaluate()的方法，Hive将调用该方法
     */
    public String evaluate(Text text) {
        String result = "手机号码错误！";
        if (text != null && text.getLength() == 11) {
            String inputStr = text.toString();
            StringBuffer sb = new StringBuffer();
            sb.append(inputStr.substring(0, 3));
            sb.append("****");
            sb.append(inputStr.substring(7));
            result = sb.toString();
        }
        return result;
    }

}

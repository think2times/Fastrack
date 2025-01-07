package spark.demo

import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{DataFrame, Dataset, Row, SparkSession}
import org.apache.spark.sql.types._

/**
  * 使用SparkSQL、RDD和DataFrame查询v_person表数据，并按age字段降序排列
  */
object SparkSQLDemo {

  def main(args: Array[String]): Unit = {

    //构建SparkSession
    val session=SparkSession.builder()
      .appName("")
      .master("local[*]")
      .getOrCreate()

    //读取HDFS数据，创建RDD
    val linesRDD: RDD[String] = session.sparkContext.textFile("hdfs://centos01:9000/input/person.txt")
    //将RDD中的每一行数据转为Person2对象
    val personRDD: RDD[Person2] = linesRDD.map(line => {
      val fields = line.split(",")
      val id = fields(0)
      val name = fields(1)
      val age = fields(2)
      Person2(id, name, age)
    })
    /*val schema=StructType(
      List{
        StructField("id",StringType,true)
        StructField("name",StringType,true)
        StructField("age",StringType,true)
      }
    )*/

    //导入隐式转换
    import session.implicits._
    //将RDD转换为DataFrame
    var pdf = personRDD.toDF()
    //创建临时视图
    pdf.createTempView("v_person")
    //执行查询
    val result: DataFrame = session.sql("select * from v_person order by age desc")
    //显示查询结果
    result.show()
    //关闭SparkSession
    session.close()

  }

}
case class Person2(id:String,name:String,age:String)
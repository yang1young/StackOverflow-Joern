import com.sun.org.apache.xpath.internal.SourceTree;
import com.sun.scenario.effect.impl.sw.sse.SSEBlend_SRC_OUTPeer;
import org.apache.commons.lang.StringEscapeUtils;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;


/**
 * Created by Qiao Yang on 28/12/2016.
 */

public class GetCppCode {


    public void getAllCppQA(){
        DatabaseOp questionOp = new DatabaseOp();
        String sql = "select Id,Body,Tags from Posts where PostTypeId = 1 and (Tags LIKE '%<c++11>%' OR Tags LIKE '%<visual-c++>%')";
        ResultSet rsQuestion = questionOp.search(sql);
        int count = 887602;
        int quesNum = 0;
        try {
            while (rsQuestion.next()) {
                quesNum++;
                String question = RegexUtils.codeClean(rsQuestion.getString("Body"));
                String tags = RegexUtils.tagsClean(rsQuestion.getString("Tags"));
                String questionId = rsQuestion.getString("Id");

                if (question != null) {
                   count++;
                   //insertToDatabase(questionOp, count, question, tags);
                }
                //get answers
                 LinkedList<String> answers = getAnswer(questionId, questionOp);
                 Iterator<String> it = answers.iterator();
                 while (it.hasNext()) {
                     String currentAnswer = it.next();//RegexUtils.codeClean(it.next());
                     if (currentAnswer != null) {
                         count++;
                         //insertToDatabase(questionOp, count, currentAnswer, tags);
                        }
                    }
            }
            questionOp.disConnect();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }


    public void insertToDatabase(DatabaseOp questionOp, int num, String text, String tags) {

        String sqlInsert = "insert into SampleC(Id,Code,Tags)" + "values('" + num + "','" + text + "', '" + tags + "')";
        questionOp.insert(sqlInsert);
    }


    public static LinkedList<String> getAnswer(String id, DatabaseOp questionOp) throws Exception {

        LinkedList<String> list = new LinkedList<String>();

        String sqlFindAnswer = "select Body from Posts where ParentId =" + "'" + id + "'";
        ResultSet rsAnswer = questionOp.search(sqlFindAnswer);
        while (rsAnswer.next()) {
            String answerTemp = RegexUtils.codeClean(rsAnswer.getString("Body"));
            if (answerTemp != null) {
                list.add(answerTemp);
            }
        }
        return list;
    }


    /*public static HashMap<String, String> getAllData(ResultSet rsQuestion, String[] answers) throws Exception {


        HashMap<String, String> resultMap = new HashMap<String, String>();
        resultMap.put("score", rsQuestion.getString("Score"));
        resultMap.put("id", rsQuestion.getString("Id"));
        resultMap.put("title", RegexUtils.codeClean(rsQuestion.getString("Title")));
        resultMap.put("tags", rsQuestion.getString("Tags"));
        resultMap.put("question", RegexUtils.codeClean(rsQuestion.getString("Body")));

        for (int j = 0; j < answers.length; j++) {
            resultMap.put("answers" + j, answers[j]);
        }
        return resultMap;

    }*/
}


//sample Q&A Posts data
/*
Id                   4
PostTypeId           1
AcceptedAnswerId     7
ParentId             null
CreationDate         2008-07-31 21:42:53.0
Score                441
ViewCount            29333
Body                 <p>I want to use a track-bar to change a form's opacity.</p>&#xA;&#xA;<p>This is my code:
                     </p>&#xA;&#xA;<pre><code>decimal trans = trackBar1.Value / 5000;&#xA;this.Opacity = trans;&#xA;
                     </code></pre>&#xA;&#xA;<p>When I try to build it, I get this error:</p>&#xA;&#xA;<blockquote>&#xA;
                     <p>Cannot implicitly convert type 'decimal' to 'double'.</p>&#xA;</blockquote>&#xA;&#xA;
                     <p>I tried making <code>trans</code> a <code>double</code>, but then the control doesn't work.
                     This code has worked fine for me in VB.NET in the past. </p>&#xA;
OwnerUserId          8
OwnerDisplayName     null
LastEditorUserId     5455605
LastEditorDisplyName null
LastEditDate         2015-12-23 21:34:29.0
LastActivityDate     2016-07-17 20:33:18.0
Title                When setting a form's opacity should I use a decimal or double?
Tags                 <c#><winforms><type-conversion><decimal><opacity>
AnswerCount          13
CommentCount         3
FavoriteCount        36
ClosedDate           2016-12-29 11:05:43.0
CommunityOwnedDate   2012-10-31 16:42:47.0
*/

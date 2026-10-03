@IsTest
private class AsterPipelineControllerTest {
    @IsTest
    static void classifiesThreeLevelsAndDoesNotMutateRecords() {
        Date todayDate = Date.newInstance(2026, 9, 29);
        List<Opportunity> rows = new List<Opportunity>{
            new Opportunity(Name='Healthy', StageName='Prospecting', CloseDate=todayDate.addDays(30), Amount=15000, NextStep='Discovery call'),
            new Opportunity(Name='Attention', StageName='Prospecting', CloseDate=todayDate.addDays(30), Amount=9000),
            new Opportunity(Name='Critical', StageName='Prospecting', CloseDate=todayDate.addDays(-2), Amount=0)
        };
        Test.startTest();
        AsterPipelineController.PipelineSummary result = AsterPipelineController.summarize(rows, todayDate);
        Test.stopTest();
        System.assertEquals(3, result.reviewed);
        System.assertEquals(1, result.healthy);
        System.assertEquals(1, result.attention);
        System.assertEquals(1, result.critical);
        System.assertEquals(24000, result.openAmount);
        System.assertEquals('Missing next step; Overdue close date; Missing or invalid amount', result.rows[2].reasons);
        System.assertEquals(-2, result.rows[2].daysToClose);
        System.assertEquals(0, rows[2].Amount);
    }
    @IsTest
    static void emptyPipelineIsSafe() {
        AsterPipelineController.PipelineSummary result = AsterPipelineController.summarize(new List<Opportunity>(), Date.today());
        System.assertEquals(0, result.reviewed);
        System.assertEquals(0, result.openAmount);
        System.assertEquals(0, result.rows.size());
    }
}
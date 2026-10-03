@IsTest
private class AsterPipelinePageControllerTest {
    @IsTest
    static void readsOnlyPortfolioAccountAndMemoizesSummary() {
        Account included = new Account(Name='Aster Portfolio Lab (fictional)');
        Account excluded = new Account(Name='Other demo account (fictional)');
        insert new List<Account>{included, excluded};
        insert new List<Opportunity>{
            new Opportunity(Name='Included scenario', AccountId=included.Id, StageName='Prospecting', CloseDate=Date.today().addDays(10), Amount=12000, NextStep='Book review'),
            new Opportunity(Name='Excluded scenario', AccountId=excluded.Id, StageName='Prospecting', CloseDate=Date.today().addDays(10), Amount=99999)
        };
        Test.startTest();
        AsterPipelinePageController page = new AsterPipelinePageController();
        AsterPipelineController.PipelineSummary first = page.getSummary();
        AsterPipelineController.PipelineSummary second = page.getSummary();
        Test.stopTest();
        System.assertEquals(1, first.reviewed);
        System.assertEquals(1, first.healthy);
        System.assertEquals(12000, first.openAmount);
        System.assertEquals('Included scenario', first.rows[0].name);
        System.assertEquals(first, second);
    }
}

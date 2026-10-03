List<OpportunityStage> stages = [SELECT MasterLabel FROM OpportunityStage WHERE IsActive = true AND IsClosed = false ORDER BY SortOrder LIMIT 1];
System.assert(!stages.isEmpty(), 'An open opportunity stage is required');
Account sample = new Account(Name='Aster Portfolio Lab (fictional)', Industry='Technology', Description='Synthetic portfolio scenario; not a customer engagement.');
insert sample;
String openStage = stages[0].MasterLabel;
insert new List<Opportunity>{
 new Opportunity(Name='Aster | Discovery expansion (fictional)', AccountId=sample.Id, StageName=openStage, CloseDate=Date.today().addDays(32), Amount=32000, NextStep='Hold discovery workshop', Description='Synthetic healthy pipeline case.'),
 new Opportunity(Name='Aster | Proposal handoff (fictional)', AccountId=sample.Id, StageName=openStage, CloseDate=Date.today().addDays(18), Amount=18000, Description='Synthetic missing-next-step case.'),
 new Opportunity(Name='Aster | At-risk renewal (fictional)', AccountId=sample.Id, StageName=openStage, CloseDate=Date.today().addDays(-8), Amount=0, Description='Synthetic overdue and amount-quality case.')
};
System.debug('ASTER_PORTFOLIO_DATA_CREATED ' + sample.Id);

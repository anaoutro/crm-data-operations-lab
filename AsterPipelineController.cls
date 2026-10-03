public with sharing class AsterPipelineController {
    public class OpportunityRow {
        @AuraEnabled public Id id {get; set;}
        @AuraEnabled public String name {get; set;}
        @AuraEnabled public String ownerName {get; set;}
        @AuraEnabled public String stageName {get; set;}
        @AuraEnabled public Decimal amount {get; set;}
        @AuraEnabled public Date closeDate {get; set;}
        @AuraEnabled public String nextStep {get; set;}
        @AuraEnabled public Integer daysToClose {get; set;}
        @AuraEnabled public String severity {get; set;}
        @AuraEnabled public String reasons {get; set;}
    }
    public class PipelineSummary {
        @AuraEnabled public Integer reviewed {get; set;}
        @AuraEnabled public Integer critical {get; set;}
        @AuraEnabled public Integer attention {get; set;}
        @AuraEnabled public Integer healthy {get; set;}
        @AuraEnabled public Decimal openAmount {get; set;}
        @AuraEnabled public List<OpportunityRow> rows {get; set;}
        public PipelineSummary() {
            reviewed = 0; critical = 0; attention = 0; healthy = 0;
            openAmount = 0; rows = new List<OpportunityRow>();
        }
    }
    @AuraEnabled(cacheable=true)
    public static PipelineSummary getPipeline() {
        List<Opportunity> records = [
            SELECT Id, Name, Owner.Name, StageName, Amount, CloseDate, NextStep
            FROM Opportunity WHERE IsClosed = false AND Account.Name = 'Aster Portfolio Lab (fictional)'
            WITH USER_MODE ORDER BY CloseDate ASC LIMIT 500
        ];
        return summarize(records, Date.today());
    }
    @TestVisible
    private static PipelineSummary summarize(List<Opportunity> records, Date todayDate) {
        PipelineSummary result = new PipelineSummary();
        for (Opportunity item : records) {
            OpportunityRow row = new OpportunityRow();
            row.id = item.Id;
            row.name = item.Name;
            row.ownerName = item.Owner == null ? 'Unassigned' : item.Owner.Name;
            row.stageName = item.StageName;
            row.amount = item.Amount;
            row.closeDate = item.CloseDate;
            row.nextStep = item.NextStep;
            row.daysToClose = item.CloseDate == null ? null : todayDate.daysBetween(item.CloseDate);
            List<String> issues = new List<String>();
            if (String.isBlank(item.NextStep)) issues.add('Missing next step');
            if (item.CloseDate != null && item.CloseDate < todayDate) issues.add('Overdue close date');
            if (item.Amount == null || item.Amount <= 0) issues.add('Missing or invalid amount');
            row.reasons = String.join(issues, '; ');
            row.severity = issues.size() >= 2 ? 'Critical' : issues.size() == 1 ? 'Attention' : 'Healthy';
            if (row.severity == 'Critical') result.critical++;
            else if (row.severity == 'Attention') result.attention++;
            else result.healthy++;
            result.reviewed++;
            if (item.Amount != null && item.Amount > 0) result.openAmount += item.Amount;
            result.rows.add(row);
        }
        return result;
    }
}
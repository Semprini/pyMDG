package my.co.sample.SampleIndustry.TestDomain;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class JobHistory()
{
    
    @Column (name = "start_date")
    private Date start_date;
    
    @Id
    @Column (name = "id")
    private int id;
    
    @Column (name = "language")
    private Language language;
    
    @Expandable (name = "JobHistory", expandableClass = Employee.class)
    private Employee JobHistory;
    
    public Date getstart_date() {
        return start_date;
    }

    public void setstart_date(Date start_date) {
        this.start_date = start_date;
    }    
    
    public int getid() {
        return id;
    }

    public void setid(int id) {
        this.id = id;
    }    
    
    public Language getlanguage() {
        return language;
    }

    public void setlanguage(Language language) {
        this.language = language;
    }    
    
}
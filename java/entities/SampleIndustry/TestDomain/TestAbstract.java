package my.co.sample.SampleIndustry.TestDomain;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class TestAbstract()
{
    
    @Id
    @Column (name = "test")
    private int test;
    
    public int gettest() {
        return test;
    }

    public void settest(int test) {
        this.test = test;
    }    
    
}
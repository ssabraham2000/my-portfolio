import boto3
from botocore.client import Config
import StringIO
import zipfile

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic("arn:aws:sns:us-east-1:075339839112:deployPortfolioTopic")
    
    try:
        s3 = boto3.resource('s3')
        
        portfolio_bucket = s3.Bucket('portfolio.sonieabraham.info')
        build_bucket = s3.Bucket('portfoliobuild.sonieabraham.info')
        
        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('buildPortfolio.zip', portfolio_zip)
        
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm,
                    ExtraArgs={'ContentType': mimetype.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
            
        print "Job done!"
        topic.publish(Subject="Portfolio Deployed", Message="Portfolio was deployed succesfully")
    except:
        topic.publish(Subject="Portfolio Deploy Failed", Message="The Portfolio was not deployed succesfully")
        raise
    
    return 'Hello from Lambda'

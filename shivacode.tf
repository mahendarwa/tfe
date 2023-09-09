import { S3 } from 'aws-sdk';

export const handler = async (event, context) => {
  const s3 = new S3();
  
  const bucketName = 'www.enlume.com';
  const objectKeyPrefix = 'www.enlume.com/media-images/';
  
  try {
    // List all object versions in the specified S3 bucket and prefix
    const objectVersions = await s3.listObjectVersions({
      Bucket: bucketName,
      Prefix: objectKeyPrefix,
    }).promise();

    // Extract older versions (excluding the latest) for deletion
    const versionsToDelete = objectVersions.Versions.slice(1);

    if (versionsToDelete.length > 0) {
      // Create a list of objects to delete
      const objectsToDelete = versionsToDelete.map(({ Key, VersionId }) => ({
        Key,
        VersionId,
      }));

      // Delete the older versions
      await s3.deleteObjects({
        Bucket: bucketName,
        Delete: { Objects: objectsToDelete },
      }).promise();
    }

    return {
      statusCode: 200,
      body: JSON.stringify('Cache cleared successfully'),
    };
  } catch (error) {
    console.error('Error clearing cache:', error);

    return {
      statusCode: 500,
      body: JSON.stringify('Error clearing cache'),
    };
  }
};

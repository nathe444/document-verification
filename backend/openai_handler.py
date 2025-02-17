import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Optional

class OpenAIHandler:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Validate OpenAI API key
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is missing. Please set OPENAI_API_KEY in .env file.")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    def _get_prompt(self, prompt_type: str) -> str:
        """
        Define predefined prompts for different analysis types
        """
        prompts: Dict[str, str] = {
            'factual_accuracy_verification': """Can you review this script to verify that all the information is 100% factual? Please follow these steps:
1.Break the Script into Claims:
oBreak your script into individual factual claims or statements.
2.Cross-Check Claims:
oFor each claim, first cross-check the information against the sources you provided (if available). If the sources are absent or do not seem credible, cross-check the claims against reliable and trustworthy online sources.
3.Check Consistency:
oEnsure that the facts are consistent with each other within your script and are logical in context.
4.Flag Ambiguities:
oIf any claim is ambiguous, unclear, or cannot be verified, flag it as requiring further clarification.
5.Knowledge Cutoff:
oIf a claim references information beyond the system's knowledge cutoff, respond with 'knowledge cutoff reached.'
6.Verify Accuracy:
oIf all claims are verified and accurate, respond with 'Yes, it's all factual.'
oIf any claims are not accurate or cannot be verified, respond with 'No, there are inaccuracies' and specify the exact number of inaccuracies, using the format 'Exactly [number] claims are inaccurate.'
Provide Suggestions for Fixing Inaccuracies:
If the response is 'No, there are inaccuracies,' provide a detailed breakdown for you, listing each inaccurate claim and offering specific suggestions on how to correct it (e.g., updating information, removing unsupported claims, or finding more reliable sources).
Instruction:
Please provide the final Possible Output based on the steps above. Conduct a thorough analysis, taking the necessary time to evaluate the response, and then output only one of the following:
1.Yes, it's all factual
oReason: 'All claims in your script are accurate and verified.'
oExplanation: No further changes are required, and the content is factually sound.
2.No, there are inaccuracies
oReason: 'Exactly [number] claims are inaccurate.'
oDetailed Breakdown of Fixes Needed:
Inaccuracy 1: '[Insert inaccurate claim]' is factually incorrect based on [insert source or reasoning]. Consider revising the claim to reflect [insert correct information].
Inaccuracy 2: '[Insert inaccurate claim]' does not match the data from [insert source]. Update the claim with information from a more reliable or recent source.
(Continue for each inaccurate claim)
oFix Suggestions:
Update Facts: 'For [specific claim], update the information with the correct data from a reliable source such as [insert source].'
Remove Unsupported Claims: 'The claim about [specific topic] is not supported by any credible sources. Consider removing it or finding a reliable source to back it up.'
Clarify Ambiguous Statements: 'The statement regarding [specific topic] is too vague and needs clarification. Provide more detail or context to ensure accuracy.'
3.Knowledge cutoff reached
oReason: 'Some claims reference information beyond the system's knowledge cutoff.'
oExplanation: The claims could not be verified because they involve information beyond the system's current knowledge. You may need to fact-check those claims using up-to-date sources.
Important:
Always provide a detailed breakdown for 'No, there are inaccuracies' responses, specifying which claims are inaccurate and what needs to be corrected.
For 'Yes, it's all factual,' confirm that no further changes are needed.
For 'Knowledge cutoff reached,' clearly state that the information exceeds the system's knowledge and recommend further fact-checking
""",
            'source_verification': """Can you review the content to ensure that all the information presented aligns 100% with the sources listed by the writer? Please follow these steps:
1.Locate Sources:
oLocate the section of the document under the subheading 'Links' or 'Sources' where URLs are provided.
oIf no sources are listed, respond with 'No sources provided' along with the statement 'You did not include any URLs for verification.'
2.Validate Sources:
oIf sources are listed, extract and validate the URLs.
3.Map Claims to Sources:
oMap each claim in the article to the appropriate source from the list of URLs.
oFor each claim, verify whether the information in the article is fully supported by the content from the provided sources.
4.Assess Source Support:
oIf all claims are supported by the sources, respond with 'Yes, sources check out' along with the statement 'All your claims are supported by the provided sources.'
oIf any claims are not supported by the sources or if a source does not match the content, respond with 'No, sources do not check out' and provide the exact number of unsupported claims, using the format 'Exactly [number] of your claims are not supported by the provided sources.'
5.Detailed Breakdown of Issues:
oIf 'No, sources do not check out,' follow with a detailed breakdown listing the specific claims that are not supported, identifying the mismatched source(s), and explaining what corrections are needed for each unsupported claim.
oThe breakdown should include the following information for each unsupported claim:
1.Claim: Clearly state the claim that is not supported by the source.
2.Mismatched Source: Identify the specific source that does not match the claim.
3.Suggested Fix: Provide suggestions on how you can correct the claim (e.g., rewording, finding a more appropriate source, or verifying the information).
Instruction: After you complete the analysis, output the final result along with a detailed breakdown, if necessary. Conduct a thorough analysis, taking the necessary time to evaluate the response, and then output the following:
Final Output: One of these three options:
1.Yes, sources check out
Reason: 'All your claims are supported by the provided sources.'
Explanation: No further issues are found. No changes needed.
2.No, sources do not check out
Reason: 'Exactly [number] of your claims are not supported by the provided sources.'
Detailed Breakdown:
Claim 1: '[Insert unsupported claim]' is not backed by the source '[Insert mismatched URL].' Consider rewording the claim or finding a more relevant source.
Claim 2: '[Insert unsupported claim]' contains information that differs from the content in '[Insert mismatched URL].' Verify the claim against the source or update it.
(Continue for each unsupported claim)
3.No sources provided
Reason: 'You did not include any URLs for verification.'
Explanation: The document does not contain any URLs for verification. Consider adding reliable sources to back up your claims.
Important:
Always provide a detailed breakdown for 'No, sources do not check out' responses, specifying exactly which of your claims are unsupported, which sources are mismatched, and how to fix the issues. For 'No sources provided,' suggest adding relevant sources for claims verification.
""",
            'detail_verification': """Can you review this script to determine if the content is detailed enough to fully address and solve the reader's problem while remaining brief and to the point? Please follow these steps:
1.Identify the Core Problem:
oIdentify the core problem or question your script is addressing.
2.Evaluate the Solution:
oEvaluate whether the solution you provided is complete and includes all necessary steps to solve the problem.
3.Check for Relevance:
oCheck that all details in your script are relevant to the solution and avoid unnecessary or unrelated information.
4.Assess the Level of Detail:
oAssess whether the level of detail is appropriate, ensuring that the reader can understand and follow the steps without confusion.
5.Avoid Unnecessary Repetition:
oDetermine if your script avoids unnecessary repetition and remains brief and to the point.
6.Account for Variations/Edge Cases:
oVerify if your content accounts for common variations or edge cases related to the problem.
7.Audience Appropriateness:
oEnsure the level of detail in your script matches the expectations and knowledge level of the intended audience.
Provide Suggestions for Fixing Issues:
If the response is 'Not detailed enough,' provide specific suggestions to help you improve the content. Break down exactly what needs to be done, such as adding more steps, removing irrelevant details, or clarifying ambiguous points.
Instruction:
Please provide the final Possible Output based on the steps above. Conduct a thorough analysis, taking the necessary time to evaluate the response, and then output only one of the following:
1.Detailed enough
oReason: 'The content fully solves the problem and remains brief and to the point.'
oExplanation: No further improvements are needed.
2.Not detailed enough
oReason: 'The content has Exactly [number] ambiguities and Exactly [number] areas that lack detail or are irrelevant.'
oDetailed Breakdown of Fixes Needed:
Ambiguities: Clearly list each ambiguity found and explain how you can clarify it (e.g., 'The step explaining how to reset the system is unclear; include more detail about the specific options in the settings menu.').
Lack of Detail: Identify areas that need more detail (e.g., 'The instructions on how to back up data are too vague; add a step-by-step process explaining how to access the backup options.').
Irrelevant Information: Specify which information is unnecessary and should be removed (e.g., 'The section about the history of the tool is irrelevant to solving the problem and should be removed.').
Fix Suggestions:
For each issue, provide a clear action you should take to improve the script, such as:
Add More Steps: 'The solution is missing key steps in the process. You should add [specific steps] to ensure the reader can follow along.'
Remove Unnecessary Information: 'There is irrelevant information in the section about [topic], which doesn't contribute to solving the problem. Consider removing it to keep the content focused.'
Clarify Ambiguities: 'Some steps are not clear enough for the intended audience. You should clarify [specific points] to avoid confusion.'
Important:
Always include a detailed breakdown when the output is 'Not detailed enough,' specifying exactly what areas need to be improved and how you can fix them. For 'Detailed enough,' provide confirmation that no further changes are needed.""",
            'technical_detail_verification': """Can you review this article for potential technical inaccuracies, inconsistencies, safety risks, and factual accuracy? Additionally, verify that the claims are supported by credible sources, both from the writer and external references. Please follow these steps:

1. Determine Presence of Technical Details:
First, assess whether the article contains technical details, such as specifications, ratings, measurements, safety instructions, or usage guidelines.
oIf no technical content is present, respond with 'No technical details found' along with the statement, 'The article does not contain any technical information that requires verification.'

2. Identify Critical Technical Information (if applicable):
If technical details are present, break the article into sections and identify key technical details, such as specifications, ratings, measurements, safety instructions, or usage guidelines. Consider the following technical aspects:
oSpecifications and Ratings
oMeasurements and Units
oTolerances and Limits
oSafety Instructions and Warnings
oUsage Guidelines and Best Practices
oComponent Descriptions and Functions
oProcess and Step-by-Step Instructions
oMaterials and Durability Information
oEnergy and Power Consumption
oOperating Conditions and Environmental Factors
oMaintenance and Repair Information
oTroubleshooting and Diagnostics
oCompatibility and Interoperability

3. Cross-Check Technical Accuracy:
For each identified technical detail, cross-check it against reliable and established standards, manufacturer guidelines, or trusted sources in the relevant field. Ensure that:
oSpecifications, ratings, or measurements align with standard practices.
oSafety recommendations and usage guidelines are correct and not misleading.
oAny numerical values match industry norms or manufacturer specs.

4. Verify Sources and Cross-Check Information:
Locate and Verify Provided Sources:
oIdentify the sources provided by the writer (e.g., under a 'Sources' or 'Links' section). Check if these sources are credible and directly support the claims in the article.
oEnsure that each key technical detail is supported by an appropriate source from the writer's list. If any claims are unsupported or mismatched, flag them for correction.
Cross-Check with Reliable Online Sources:
oIf the writer’s sources are absent, incomplete, or not credible, verify the claims against reliable and trustworthy online sources, such as official documentation, industry-standard references, or academic publications.
oEnsure that the technical details are consistent with current best practices and factual information found in authoritative sources.
Assess Source Alignment:
oIf all technical claims are fully supported by the writer's sources or external credible sources, respond with 'Yes, sources check out.'
oIf any claims are not supported, respond with 'No, sources do not check out' and list the specific unsupported claims.

5. Assess the Safety Risks:
Evaluate potential safety risks associated with incorrect technical information. For each detail, consider:
oCould misleading or incorrect details lead to harm, equipment damage, or safety hazards (e.g., fire risk, mechanical failure)?
oDoes the article explain why correct specifications (e.g., proper fuse ratings) are crucial for avoiding risks?

6. Check for Contradictions or Inconsistencies:
Ensure there are no contradictions within the article. Verify that:
oInformation is consistent throughout, with no conflicting technical advice.
oInstructions and explanations follow a logical, coherent sequence.

7. Evaluate Clarity for the Reader:
Assess whether technical details are explained clearly for the intended audience. Consider:
oAre technical terms and concepts explained where necessary?
oCould any part of the article confuse the reader or lead to misinterpretation?

8. Flag Potential Errors or Ambiguities:
Identify any areas where technical information could be misunderstood or misapplied. If errors or ambiguous sections are found, flag them for correction.

9. Compare Against Industry Standards:
Compare key technical claims and safety recommendations against relevant industry standards. If the article deviates from these standards, suggest corrections to bring it in line with best practices.

Provide Suggestions for Fixing Issues:
If inaccuracies, inconsistencies, unsupported claims, or safety risks are found, provide a detailed breakdown, offering suggestions on how to fix them. For example:
oTechnical Accuracy Issue: '[Insert inaccurate technical detail]' is incorrect based on [insert source or standard]. Consider revising it to '[insert corrected detail].'
oSource Issue: '[Insert claim]' is not supported by any credible source. Either remove the claim or find a reputable source to back it up.
oSafety Risk: '[Insert detail]' poses a safety risk (e.g., fire hazard). Add a warning to ensure proper usage.
oClarity Issue: '[Insert technical explanation]' could confuse readers. Provide more context or explanation to clarify.

Instruction:
Please conduct a thorough analysis and output one of the following based on the technical accuracy and source verification of the article:
1.No technical details found:
oReason: 'The article does not contain any technical information that requires verification.'
2.Technically Accurate and Supported by Sources:
oReason: 'All technical details are accurate and supported by credible sources.'
oExplanation: No revisions needed; the article is technically sound and properly sourced.
3.Technical Issues Identified:
oReason: 'Exactly [number] technical inaccuracies or inconsistencies found.'
oDetailed Breakdown of Fixes Needed:
Inaccuracy 1: '[Insert inaccurate technical detail]' is incorrect. Correct as '[insert corrected detail].'
Safety Risk 1: '[Insert safety issue]' poses a hazard. Correct this to '[insert corrected safety detail].'
4.Unsupported Claims or Mismatched Sources:
oReason: 'Exactly [number] claims are not supported by the sources provided or external credible sources.'
oDetailed Breakdown of Fixes Needed:
Unsupported Claim 1: '[Insert claim]' is not backed by [insert source]. Either find a reliable source or remove the claim from the article.
5.Ambiguities or Misleading Information:
oReason: 'Exactly [number] areas are ambiguous or could mislead the reader.'
oDetailed Breakdown of Fixes Needed:
Ambiguity 1: '[Insert ambiguous section]' needs clarification. Suggest rewording as '[insert correction].'
6.Critical Safety Risk Identified:
oReason: 'A critical safety risk was found related to [insert issue].'
oExplanation: This must be corrected immediately to prevent hazards like overheating or mechanical failure. Correct as '[insert fix].'

Important:
Always provide a detailed breakdown for 'Technical Issues Identified,' 'Unsupported Claims,' and 'Ambiguities or Misleading Information' responses, specifying the exact issues and how they can be resolved. For 'Critical Safety Risk,' flag the issue for immediate correction
"""
        }
        
        # Add a default fallback
        return prompts.get(prompt_type, prompts['factual_accuracy_verification'])

    def process_document(
        self, 
        text: str, 
        prompt_type: str = 'factual_accuracy_verification', 
        max_tokens: Optional[int] = 1500
    ):
        # Implement token-aware text chunking
        def chunk_text(text, max_chunk_tokens=10000):
            """Split text into chunks that respect token limits."""
            import tiktoken
            
            # Use tiktoken for accurate token counting
            tokenizer = tiktoken.get_encoding("cl100k_base")
            tokens = tokenizer.encode(text)
            
            chunks = []
            for i in range(0, len(tokens), max_chunk_tokens):
                chunk_tokens = tokens[i:i+max_chunk_tokens]
                chunks.append(tokenizer.decode(chunk_tokens))
            
            return chunks

        # Chunk the text
        text_chunks = chunk_text(text)
        
        results = []
        for chunk in text_chunks:
            try:
                # Get the appropriate prompt
                prompt = self._get_prompt(prompt_type)
                
                # Create chat completion using the new OpenAI client
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": chunk}
                    ],
                    max_tokens=max_tokens
                )
                
                # Safely extract result
                result = response.choices[0].message.content.strip() if response.choices else "No response from OpenAI"
                
                if not result:
                    raise ValueError("Empty response from OpenAI API")
                
                results.append(result)
            
            except Exception as e:
                # Comprehensive error handling
                error_details = {
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "prompt_type": prompt_type
                }
                print(f"Error processing chunk: {error_details}")
        
        # If multiple chunks, generate a summary
        if len(results) > 1:
            try:
                summary_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Provide a concise, comprehensive summary of the following analysis results. Extract the key points, highlight main insights, and consolidate the information into a clear, coherent overview."},
                        {"role": "user", "content": "\n\n---\n\n".join(results)}
                    ],
                    max_tokens=max_tokens
                )
                
                summary = summary_response.choices[0].message.content.strip()
                return f"Summary of Analysis:\n{summary}\n\nDetailed Results:\n" + "\n\n---\n\n".join(results)
            except Exception as e:
                print(f"Error generating summary: {e}")
        
        # If only one chunk or summary generation fails, return original results
        return "\n\n".join(results)